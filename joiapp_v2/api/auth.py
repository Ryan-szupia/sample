from fastapi import APIRouter, HTTPException, Depends, Header
from joiapp_v2.config.firebase import db
from joiapp_v2.security.security import hash_password, decode_token, verify_token_with_refresh, create_access_token, create_refresh_token
from passlib.context import CryptContext
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from google.cloud.firestore import Transaction, firestore
from joiapp_v2.security.email import generate_verification_code, send_verification_email
import re

router = APIRouter()

# auth part

# email pattern check logic
def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# send email
@router.post("/send-verification")
async def send_verification_code(email: str, time_zone: str, transaction: Transaction):
    
    if not validate_email(email):
        raise HTTPException(400, "Invalid email format")
    
    users = db.collection("users").where("email", "==", email).get()
    if users:
        raise HTTPException(400, "Email already registered")
    
    code = generate_verification_code()
    
    now = datetime.now(ZoneInfo(time_zone))
    today = now.strftime("%Y-%m-%d")
    
    validate_doc = db.collection("users").document(email).collection("validate").document(today)
    
    if validate_doc.exists:
        
    
    
    

# signup logic
@router.post("/signup")
def signup(email: str, password: str, name: str, time_zone: str, info_agree: bool):

    try:
        create_date = datetime.now(ZoneInfo(time_zone))
    except Exception:
        raise HTTPException(400, f"Invalid timezone: {time_zone}")

    password_hash = hash_password(password)

    def signup_transaction(transaction: Transaction):
        users_ref = db.collection("users")

        query = users_ref.where("email", "==", email).limit(1)
        docs = query.stream(transaction=transaction)

        if any(docs):
            raise HTTPException(400, "Email already exists")

        user_ref = users_ref.document(email)

        transaction.set(user_ref, {
            "email": email,
            "password_hash": password_hash,
            "name": name,
            "create_date": create_date,
            "last_login_date": None,
            "time_zone": time_zone,
            "joi_point": 0,
            "role": "USER",
            "info_agree": info_agree,
            "phq9_complete": False,
            "gad7_complete": False,
            "deep_complete": False,
        })

    try:
        db.transaction()(signup_transaction)
    except Exception:
        raise HTTPException(500, "Signup failed")

    return {"message": "Signup successful"}

# login logic
@router.post("/login")
def login(email: str, password: str):
    users = db.collection("users").where("email", "==", email).get()
    if not users:
        raise HTTPException(401, "Invalid credentials")
    
    user_doc = users[0]
    user_data = user_doc.to_dict()
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    if not pwd_context.verify(password, user_data.get("password_hash")):
        raise HTTPException(401, "Password is different")

    token_data = {
        "user_id": user_doc.id,
        "email": email,
        "role": user_data.get("role"),
    }
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    if user_data.get("last_login_date") is not None:
        date = datetime.now(ZoneInfo(user_data.get("time_zone", "UTC")))
        last_date = user_data.get("last_login_date", None)
        point = user_data.get("joi_point", 0)
        
        days_diff = (date.date() - last_date.date()).days
        
        if days_diff >= 1:
            point += 5

        db.collection("users").document(user_doc.id).update({
            "last_login_date": date,
            "joi_point": point,
            "refresh_token": refresh_token,
        })
    else:
        point = 5
        date = datetime.now(ZoneInfo(user_data.get("time_zone", "UTC")))
        db.collection("users").document(user_doc.id).update({
            "last_login_date": date,
            "joi_point": point,
            "refresh_token": refresh_token,
        })
    user_data["last_login_date"] = date
    user_data["joi_point"] = point
    user_data["id"] = user_doc.id
    user_data.pop("password_hash", None)
    user_data.pop("refresh_token", None)
    
    return {
        "user": user_data,
        "message": "Login successful",
        "access_token": access_token,
    }
    
# logout logic
@router.get("/logout")
def logout(email: str):
    user_id = email
    
    db.collection("users").document(user_id).update({
        "refresh_token": None
    })

    return {"message": "Logged out successfully"}