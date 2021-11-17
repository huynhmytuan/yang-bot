
import sys
sys.path.insert(1, '../')
from db.user_utils import UserUtils
from models.user import User
import time
from firebase_admin import storage
from google.cloud.storage import Blob  

user_utils = UserUtils()
# users = user_utils.get_users()
# for user in users:
#   user.join_time = 0
# timestamp = time.time()
# user_utils.backup(users, timestamp)

check = user_utils.last_backup()
timestamp = int(check)
backup_time = time.localtime(timestamp)
format_time = time.strftime('%H:%M, Ngày %#d/%m/%Y', backup_time)
print(format_time)







