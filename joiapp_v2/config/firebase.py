import firebase_admin
from firebase_admin import credentials, firestore
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
cred_path = str(BASE_DIR / "secret" / "dev-joiapp-ver2-firebase-adminsdk-fbsvc-88924daeb1.json")

if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
    cred = credentials.ApplicationDefault()
else:
    cred = credentials.Certificate(cred_path)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()