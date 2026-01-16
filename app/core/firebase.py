import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("dev-joiapp-ver2-firebase-adminsdk-fbsvc-88924daeb1.json")

firebase_admin.initialize_app(cred)