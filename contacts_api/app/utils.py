from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="contacts_api/.env")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    try:
        encoded_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_token
    except JWTError as e:
        raise Exception(f"Error encoding JWT: {e}")

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    try:
        encoded_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_token
    except JWTError as e:
        raise Exception(f"Error encoding JWT: {e}")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        raise Exception(f"Error verifying password: {e}")

def hash_password(password: str) -> str:
    try:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hashed = pwd_context.hash(password)
        return hashed
    except Exception as e:
        raise Exception(f"Error hashing password: {e}")
