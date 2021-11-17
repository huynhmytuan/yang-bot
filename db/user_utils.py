#====DATA
import os
import sys
sys.path.insert(1, '../')
from models.user import User
from firebase_admin import db
from db.connection import DbConnection

class UserUtils:
  def __init__(self):
    self.connection = DbConnection()

  def upload_users(self, users):
    ref = db.reference(f"/users/")
    data = {}
    for user in users:
      data.update({
        user.user_id : user.asdict()
      })
    ref.update(data)

  def add_user(self, userID : int, userName):
    newUser = User()
    newUser.name = userName
    newUser.user_id = userID
    ref = db.reference(f"/users/{userID}")
    ref.update(newUser.asdict())
    
  #Lấy list user (List Object)
  def get_users(self):
    ref = db.reference(f"/users/")
    response = ref.get()
    users = []
    if not response:
      return users
    for userID in response:
      data = response[userID]
      users.append(User(**data))
    return users
    
  #Lấy 1 user (Object)
  def get_user_by_id(self, userID : int):
    ref = db.reference(f"/users/{userID}")
    data = ref.get()
    user = None
    if data:
      user = User(**data)
    return user
  
  #Xóa 1 user
  def delete_by_id(self, userID: int):
    ref = db.reference(f"/users/{userID}")
    ref.delete()


  def update_user(self, user : User):
    ref = db.reference(f"/users/{user.user_id}")
    ref.update(user.asdict())

  def get_top_by_time(self, top_type):
    ref = db.reference(f"/users/")
    response = ref.get()
    users = []
    if not response:
      return users
    for userID in response:
      data = response[userID]
      users.append(User(**data))
    return users

  #Backup dữ liệu
  def backup(self, users, time):
    for user in users:
      user.join_time = 0
    ref = db.reference(f"/users_backup/")
    data = {}
    for user in users:
      data.update({
        user.user_id : user.asdict()
      })
    ref.update({ 
      'users' : data,
      'last_backup' : time
      })
  #Check backkup
  def last_backup(self):
    ref = db.reference(f"/users_backup/")
    response = ref.get()
    last_backup = response['last_backup']
    return last_backup
  #Roll back về dữ liệu cũ
  def roll_back(self):
    backup_ref = db.reference(f"/users_backup/users/")
    response = backup_ref.get()
    ref = db.reference(f"/users/")
    ref.update(response)
    

