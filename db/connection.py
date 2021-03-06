import firebase_admin
from firebase_admin import credentials
import sys
sys.path.insert(1, '../')
from config import *

class DbConnection:
  def __init__(self):
    if not firebase_admin._apps:
      cred = credentials.Certificate("serviceAccountKey.json")
      firebase_admin.initialize_app(cred, {
        "databaseURL" : DATABASE_URL,
        'storageBucket': STORAGE_URL
      })
      print("CODE_LOG: Database is connected.")