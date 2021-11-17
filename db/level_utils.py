from models.level import Level
import sys
sys.path.insert(1, '../')
from firebase_admin import db
from db.connection import DbConnection

class LevelUtils:
  def __init__(self):
    connection = DbConnection()

  def get_levels(self):
    ref = db.reference(f"/levels/")
    respone = ref.get()
    levels = []
    if not respone:
      print("Du lieu khong the lay")
      return levels
    for level in respone:
      levels.append(Level(**level))
    return levels

  def add_user(self, newLevel):
    ref = db.reference(f"/users/{newLevel.order}")
    ref.update(newLevel.asdict())