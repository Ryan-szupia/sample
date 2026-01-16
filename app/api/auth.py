from fastapi import APIRouter, HTTPException
from app.core.firebase import db
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token

router = APIRouter()

@router.post("/signup")
def signup(email: str, password: str):
    users = db.collection("users").where("email", "==", email).get()
    if users:
        raise HTTPException(400, "Email already exists")

    db.collection("users").add({
        "email": email,
        "password_hash": hash_password(password),
        "role": "USER"
    })

    return {"message": "Signup successful"}

@router.post("/login")
def login(email: str, password: str):
    users = db.collection("users").where("email", "==", email).get()
    if not users:
        raise HTTPException(401, "Invalid credentials")

    user = users[0].to_dict()

    if not verify_password(password, user["password_hash"]):
        raise HTTPException(401, "Invalid credentials")

    return {
        "accessToken": create_access_token(users[0].id),
        "refreshToken": create_refresh_token(users[0].id)
    }