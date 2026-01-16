from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

SECRET = "JWT_SECRET"
ALGO = "HS256"

def create_access_token(user_id: str):
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=15)
    }
    return jwt.encode(payload, SECRET, algorithm=ALGO)

def create_refresh_token(user_id: str):
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(days=14)
    }
    return jwt.encode(payload, SECRET, algorithm=ALGO)