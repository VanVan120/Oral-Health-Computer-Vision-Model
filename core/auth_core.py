from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, Union
import os
import jwt
from jwt import PyJWTError as JWTError
from dotenv import load_dotenv

load_dotenv()

# Config
# Deliberately no default. An unset signing key must stop the app rather than
# fall back to a shared constant that would let anyone forge a doctor token.
SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError(
        "JWT_SECRET_KEY is not set. Generate one with:\n"
        '    python -c "import secrets; print(secrets.token_urlsafe(48))"\n'
        "then set it in your environment or .env file (see .env.example)."
    )
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300 # 5 hours for ease of demo

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
