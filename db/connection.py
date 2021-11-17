import firebase_admin
from firebase_admin import credentials
from config import *

class DbConnection:
  def __init__(self):
    if not firebase_admin._apps:
      cred = credentials.Certificate("/home/runner/Yang/serviceAccountKey.json")
      firebase_admin.initialize_app(cred, {
        "databaseURL" : DATABASE_URL,
        'storageBucket': STORAGE_URL
      })
      print("Database is connected.")