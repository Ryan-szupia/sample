from fastapi import APIRouter, HTTPException
from joiapp_v2.config.firebase import db
from joiapp_v2.config.secrets import OPENAI_API_KEY
from openai import OpenAI
from google.cloud.firestore import Transaction

router = APIRouter()

client = OpenAI(api_key=OPENAI_API_KEY)

async def create_action_items(email: str, phq9: list[int], gad7: list[int], transaction: Transaction):
    action_items = []
    
    prompt = f"""
        You are a mental health professional. Based on the following assessment history, please suggest five specific action items that would help the user.
    """
    
    user_ref = db.collection("users").document("where", "==", email).action_items.get()
    transaction.set(user_ref, {
        "itmes": action_items
    })
    
    return action_items