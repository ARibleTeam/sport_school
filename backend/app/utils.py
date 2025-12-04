import secrets
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import argon2

ph = argon2.PasswordHasher()

SECRET_KEY = "YOUR_SECRET_KEY"  # Change this in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 30 # Example


def get_password_hash(password: str) -> str:
    return ph.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    try:
        return ph.verify(hashed_password, password)
    except argon2.exceptions.VerifyMismatchError:
        return False


def create_access_token(
    subject: str | dict, expires_delta: Optional[timedelta] = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None

def generate_refresh_token() -> str:
    return secrets.token_urlsafe(32)

def create_refresh_token(
    subject: str | dict, expires_delta: Optional[timedelta] = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
