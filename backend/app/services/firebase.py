import firebase_admin
from firebase_admin import credentials, firestore
from app.config import settings

cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
firebase_app = firebase_admin.initialize_app(cred)
db = firestore.client()