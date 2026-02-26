from datetime import datetime, timedelta
from typing import Optional, Any
from jose import jwe, jwt
from passlib.context import CryptContext
import os

import hashlib
import secrets

# JWT Configuration
SECRET_KEY = "SUPER_SECRET_KEY_FOR_ENCRYPTION_CHANGE_THIS_IN_PROD"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def get_password_hash(password: str) -> str:
    salt = secrets.token_hex(8)
    h = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}${h}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        salt, h = hashed_password.split("$")
        return hashlib.sha256((plain_password + salt).encode()).hexdigest() == h
    except Exception:
        return False

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    # Sign the token (Standard JWT)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp = payload.get("exp")
        if exp is None:
            return None
        if datetime.utcfromtimestamp(exp) < datetime.utcnow():
            return None
        return payload
    except Exception:
        return None
