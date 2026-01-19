import firebase_admin
from firebase_admin import credentials, firestore
import os

cred_path = os.path.join(
    os.path.dirname(__file__),
    '..',
    'secret',
    'dev-joiapp-ver2-firebase-adminsdk.json'
)
cred = credentials.Certificate(cred_path)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()