from datetime import datetime, timedelta
from jose import jwt, JWTError
from joiapp_v2.config.firebase import db
from passlib.context import CryptContext
from fastapi import HTTPException, Header
from joiapp_v2.config.secrets import JWT_SECRET_KEY
from joiapp_v2.config.jwt import (
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
)
#Password encryption
def hash_password(password: str):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    hashed_password = pwd_context.hash(password)
    return hashed_password
    
#Create access token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)

#Create a refresh token
def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)

#Retrieve token information
def decode_token(token: str):
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])

#Token Verification
def verify_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(401, "Authorization header missing")
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(401, "Invalid authentication scheme")
    except ValueError:
        raise HTTPException(401, "Invalid authorization header format")
    
    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            raise HTTPException(401, "Invalid token type")
        
        # Expiration check is automatically done by jwt.decode
        return payload
    except JWTError:
        raise HTTPException(401, "Invalid or expired token")
    
#Create an access token with a refresh token
def refresh_access_token(refresh_token: str):
    try:
        payload = decode_token(refresh_token)
        
        if payload.get("type") != "refresh":
            raise HTTPException(401, "Invalid token type")
        
        user_id = payload.get("user_id")
        
        user_doc = db.collection("users").document(user_id).get()
        if not user_doc.exists:
            raise HTTPException(401, "User not found")
        
        user_data = user_doc.to_dict()
        if user_data.get("refresh_token") != refresh_token:
            raise HTTPException(401, "Invalid refresh token")
        
        token_data = {
            "user_id": user_id,
            "email": payload.get("email")
        }
        new_access_token = create_access_token(token_data)
        
        return {
            "access_token": new_access_token,
        }
    except JWTError:
        raise HTTPException(401, "Invalid or expired refresh token")