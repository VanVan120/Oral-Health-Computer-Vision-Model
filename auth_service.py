from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from datetime import timedelta
from pydantic import BaseModel
from database import get_session
from models import User
from auth_core import verify_password, get_password_hash, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM, jwt, JWTError

# Auth Router
router = APIRouter(prefix="/auth", tags=["authentication"])

# Deps
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    name: str
    role: str

class UserCreate(BaseModel):
    email: str
    password: str
    name: str
    role: str = "patient" # default

async def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    if user is None:
        raise credentials_exception
    return user

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    # 1. Fetch User
    statement = select(User).where(User.email == form_data.username)
    user = session.exec(statement).first()
    
    # 2. Verify Pwd
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Generate Token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user_id": user.id,
        "name": user.name,
        "role": user.role
    }

@router.post("/register", response_model=Token)
async def register_user(user_data: UserCreate, session: Session = Depends(get_session)):
    # Check if exists
    if session.exec(select(User).where(User.email == user_data.email)).first():
        raise HTTPException(status_code=400, detail="Email already registered")
        
    hashed_pwd = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email, 
        password_hash=hashed_pwd,
        name=user_data.name,
        role=user_data.role
    )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    # Auto-login
    access_token = create_access_token(data={"sub": db_user.email, "role": db_user.role})
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user_id": db_user.id,
        "name": db_user.name,
        "role": db_user.role
    }

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    role: str | None = None

@router.get("/users", response_model=list[dict])
async def get_all_users(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    if current_user.role != "doctor":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    users = session.exec(select(User).where(User.role == "patient")).all()
    # Return safe data
    return [{"id": u.id, "name": u.name, "email": u.email, "role": u.role} for u in users]

@router.get("/doctors", response_model=list[dict])
async def get_all_doctors(session: Session = Depends(get_session)):
    """Get all doctors for appointment booking - no auth required for listing"""
    doctors = session.exec(select(User).where(User.role == "doctor")).all()
    # Return safe data (id and name only)
    return [{"id": d.id, "name": d.name} for d in doctors]

@router.put("/users/{user_id}", response_model=dict)
async def update_user(user_id: int, user_update: UserUpdate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    if current_user.role != "doctor":
        raise HTTPException(status_code=403, detail="Not authorized")
        
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if user_update.name:
        user.name = user_update.name
    if user_update.email:
         # Optional: Check email uniqueness if changing email
        user.email = user_update.email
    
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return {"id": user.id, "name": user.name, "email": user.email, "role": user.role}

class PasswordChange(BaseModel):
    current_password: str
    new_password: str

@router.post("/change-password")
async def change_password(password_data: PasswordChange, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    # Verify current password
    if not verify_password(password_data.current_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    # Hash new password and update
    new_hash = get_password_hash(password_data.new_password)
    current_user.password_hash = new_hash
    
    session.add(current_user)
    session.commit()
    
    return {"message": "Password updated successfully"}
