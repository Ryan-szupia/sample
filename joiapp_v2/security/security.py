from datetime import datetime, timedelta
from jose import jwt, JWTError
from joiapp_v2.config.firebase import db
from passlib.context import CryptContext
from fastapi import HTTPException, Header, Response, Depends
from joiapp_v2.config.secrets import JWT_SECRET_KEY
from joiapp_v2.config.jwt import (
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
)
from typing import Optional
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
def verify_token_with_refresh(response: Response, authorization: str = Header(None)):
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
    except JWTError as e:
        if "expired" in str(e).lower():
            try:
                unverified_payload = jwt.decode(
                    token,
                    options={"verify_signature": False, "verify_exp": False}
                )
                user_id = unverified_payload.get("user_id")
                
                if not user_id:
                    raise HTTPException(401, "Invalid token")
                
                user_doc = db.collections("users").document(user_id).get()
                if not user_doc.exists:
                    raise HTTPException(401, "User not found")
                
                user_data = user_doc.to_dict()
                refresh_token = user_data.get("refresh_token")
                
                if not refresh_token:
                    raise HTTPException(401, "No refresh token")
                
                try:
                    refresh_payload = decode_token(refresh_token)
                    
                    if refresh_payload.get("type") != "refresh":
                        raise HTTPException(401, "Invalid refresh token type")
                    
                    token_data = {
                        "user_id": user_id,
                        "email": user_data.get("email"),
                        "role": user_data.get("role"),
                    }
                    new_access_token = create_access_token(token_data)
                    response.headers["x-new-access-token"] = new_access_token
                    
                    new_payload = decode_token(new_access_token)
                    return new_payload
                
                except JWTError:
                    raise HTTPException(401, "Refresh token expired")
            
            except Exception:
                raise HTTPException(401, "Token refresh failed")
        else:
            raise HTTPException(401, "Invalid token")

# get current user
def get_current_user(
    response: Response,
    payload: dict = Depends(verify_token_with_refresh)
):
    user_id = payload.get("user_id")
    user_doc = db.collection("users").document(user_id).get()
    
    if not user_doc.exists:
        raise HTTPException(404, "User not found")
    
    return user_doc.to_dict()
                
# user role check
def require_role(required: str):
    def role_checker(
        response: Response,
        current_user: dict = Depends(get_current_user)
    ):
        user_role = current_user.get("role", "USER")
        
        role_hierarchy = {
            "USER": 0,
            "ADMIN": 1,
        }
        
        if role_hierarchy.get(user_role, 0) < role_hierarchy.get(require_role, 0):
            raise HTTPException(403, "Insufficient permissions")
            
        return current_user
    
    return role_checker