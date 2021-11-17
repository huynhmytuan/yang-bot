import json
import aiocron
import os
import time
from replit import db
from db.user_utils import UserUtils
from models.user import User

os.environ['TZ'] = 'Asia/Ho_Chi_Minh'
time.tzset()
user_utils = UserUtils()
# Everyday at 00:05
@aiocron.crontab('2 0 * * *', start=False)
async def reset_day():
  users = user_utils.get_users()  
  if users:
    for user in users:
      if user.day_learning != 0:
        user.day_learning = 0
    user_utils.upload_users(users)
    with open("log.txt", "a") as file_object:
      file_object.write(f"\n'=============Daily reset!============='")        
# Weekly at 00:06 on monday of week
@aiocron.crontab('4 0 * * MON', start=False)
async def reset_week():
  users = user_utils.get_users()  
  if users:
    with open('users_backup.json', 'w') as b:
      json_str = [user.__dict__ for user in users]
      for user in users:
        user.join_time = 0
      b.seek(0)
      json.dump(json_str, b, indent=4)
      b.close()
      timestamp = time.time()
      db['last_backup'] = timestamp
    for user in users:
      if user.week_learning != 0:
        user.week_learning = 0
    user_utils.upload_users(users)
    with open("log.txt", "a") as file_object:
      file_object.write(f"\n=============Weekly reset!=============")      


# Monthly at 00:10 on day 1 of month
@aiocron.crontab('0 6 0 1 * *', start=False)
async def reset_month():
  users = user_utils.get_users()  
  if users:
    for user in users:
      if user.month_learning != 0:
        user.month_learning = 0
    user_utils.upload_users(users)
    with open("log.txt", "a") as file_object:
      file_object.write(f"\n'=============Monthly reset!============='") 

def Run_Scheduler():
    reset_day.start()
    reset_week.start()
    reset_month.start()
