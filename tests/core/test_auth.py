import pytest
from core.auth_core import verify_password, get_password_hash, create_access_token
import jwt
from core.auth_core import SECRET_KEY, ALGORITHM

def test_password_hashing():
    password = "secret_password"
    hashed = get_password_hash(password)
    
    assert password != hashed
    assert verify_password(password, hashed) is True
    assert verify_password("wrong_password", hashed) is False

def test_create_access_token():
    data = {"sub": "testuser"}
    token = create_access_token(data)
    
    assert isinstance(token, str)
    
    # Verify the token can be decoded
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded["sub"] == "testuser"
    assert "exp" in decoded
