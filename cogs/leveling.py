import time
from discord.ext import commands
from discord.utils import get
import sys
sys.path.insert(1, '../')
from db.user_utils import UserUtils
from models.user import User
from db.level_utils import LevelUtils
from helpers.custom_function import time_readable
from config import *

class leveling(commands.Cog):
  def __init__(self, bot):
      self.bot = bot
      self.GUILD_ID = GUILD_ID
      self.ADMIN_CHANNEL_ID = ADMIN_CHANNEL_ID
      # Study categories name in lowcase
      self.categories = ['book room','study hub']
      self.user_utils = UserUtils()
      self.level_utils = LevelUtils()

  @commands.command(
      brief='Khởi tạo dữ liệu toàn bộ người dùng trong hệ thống.',
      aliases=['cd'])

  async def create(self, ctx):
    if ctx.message.channel == self.bot.get_channel(self.ADMIN_CHANNEL_ID):
      users = self.user_utils.get_users()
      list_mem = [member for member in ctx.guild.members if not member.bot]
      if not users:
        await ctx.send("Đang khởi tạo dữ liệu người dùng")
        new_users = []
        for user in list_mem:
          new_user = User(user_id = user.id, name = user.name)
          new_users.append(new_user)
        self.user_utils.upload_users(new_users)
        await ctx.send("Omedetou Oni-chan!\nYang đã giúp oni-chan tạo hết dữ liệu người dùng rồi đó, khen Yang điii! Hehe 😊")
      else:
        addedMems = 0
        new_users = []
        for user in list_mem:
          if user.id not in [user.user_id for user in users]:
            addedMems += 1
            new_user = User(user_id = user.id, name = user.name)
            new_users.append(new_user)
        if addedMems == 0:
          await ctx.send(f"Tất cả thành viên đã được cập nhật. Không có thành viên mới nào.")
        else:
          self.user_utils.upload_users(new_users)
          await ctx.send(f"Đã thêm mới {addedMems} thành viên.")

  def check_and_add_user(self, new_user):
    #Get list user
    users = self.user_utils.get_users()
    if new_user.id not in [user.user_id for user in users]:
      print("+ User not in database. Adding..")
      self.user_utils.add_user(new_user.id, new_user.name)
      print("+ User Added!")

  def remove_user(self, leave_user):
    #Get list user
    users = self.user_utils.get_users()
    for user in users:
      if  user.user_id == leave_user.id:
        self.user_utils.delete_by_id(user.user_id)
        break
  async def add_study_role(self, member):
    member_roles = member.roles
    if STUDY_ROLE_ID not in [role.id for role in member_roles]:
      study_role = get(member.guild.roles, id=STUDY_ROLE_ID)
      await member.add_roles(study_role)
    else:
      pass
  async def remove_study_role(self, member):
    member_roles = member.roles
    if STUDY_ROLE_ID in [role.id for role in member_roles]:
      study_role = get(member.guild.roles, id=STUDY_ROLE_ID)
      await member.remove_roles(study_role)
    else:
      pass
  async def add_role(self, member):
    levels = []
    member_roles = member.roles
    levels = self.level_utils.get_levels()
    user = self.user_utils.get_user_by_id(member.id)
    semester_time = user.semester_learning
    # Check time is more than end of last rank
    if semester_time >= levels[-1].end:
      return
    else:
      for level in levels:
        #Get Current Time Level
        if semester_time >= level.mark and semester_time < level.end:
          if level.id in [role.id for role in member_roles]:
            pass
          else:
            user.current_level = level.order
            print(f'ROLE_UPDATE: {member.name} role has been added:',level.name)
            if user.highest_rank < level.order:
              user.highest_rank = level.order
            new_role = get(member.guild.roles, id=level.id)
            await member.add_roles(new_role)
          #====================================
        elif level.id in [role.id for role in member_roles]:
            #remove current role
          cur_role = get(member.guild.roles, id=level.id)
          await member.remove_roles(cur_role)
      self.user_utils.update_user(user)

  def startLearning(self, member):
    user = self.user_utils.get_user_by_id(member.id)
    if not user: 
      leveling.check_and_add_user(self, member)
      user = self.user_utils.get_user_by_id(member.id)
    if member.id == user.user_id:
      if user.join_time != 0:
        return
      user.join_time = time.time()
      # break
    self.user_utils.update_user(user)

  def endLearning(self, member):
    user = self.user_utils.get_user_by_id(member.id)
    if member.id == user.user_id:
      if user.join_time == 0:
        return 
      #calculate section learn time:
      now = time.time()
      learn_time = (now - user.join_time) / 3600
      if learn_time < 0.017:
        user.join_time = 0
        self.user_utils.update_user(user)
        return
      join = time.localtime(user.join_time)
      end = time.localtime(now)
      print(f"\nLEARNING_LOG: {member.name} | ID: {member.id} | Start: {time.strftime('%H:%M, %#d/%m/%Y', join)} | End: {time.strftime('%H:%M, %#d/%m/%Y', end)} | Time: {time_readable(learn_time)}| Before: {user.learning_time}")
      #Update total learning time
      user.learning_time += learn_time
      user.day_learning += learn_time
      user.month_learning += learn_time
      user.week_learning += learn_time
      user.semester_learning += learn_time
      user.join_time = 0
    self.user_utils.update_user(user)

  @commands.Cog.listener()
  async def on_member_join(self, member):
    if not member.bot:
      print(f"SERVER_LOG: Member {member.name} ID: {member.id} join server")
      leveling.check_and_add_user(self, member)

  @commands.Cog.listener()
  async def on_voice_state_update(self, member, before, after):
    if not member.bot:
      #Connect to Study Room
      if not before.channel and after.channel: 
        after_category_name = str.lower(after.channel.category.name)
        if any(word in after_category_name for word in self.categories):
          await leveling.add_study_role(self, member)
      #==================================================
      if before.channel and after.channel:
        before_name = str.lower(before.channel.category.name)
        after_name = str.lower(after.channel.category.name)
        # Move from non-study to Study Room
        if not any(word in before_name for word in self.categories) and any(word in after_name for word in self.categories):
          await leveling.add_study_role(self, member)
        #Check video in study room
        if any(word in before_name for word in self.categories) and any(word in after_name for word in self.categories):
          if member.voice.self_video or member.voice.self_stream:
              leveling.startLearning(self, member)
          elif not member.voice.self_video and not member.voice.self_stream:
            leveling.endLearning(self, member)
            #Check and add new role
            await leveling.add_role(self, member)
        #Move to non-study room
        elif any(word in before_name for word in self.categories) and not any(word in after_name for word in self.categories):
          leveling.endLearning(self, member)
          await leveling.add_role(self, member)
          await leveling.remove_study_role(self, member)
      elif before.channel and not after.channel:
        before_name = str.lower(before.channel.category.name)
        #Quit study room
        if any(word in before_name for word in self.categories):
          leveling.endLearning(self, member)
          await leveling.add_role(self, member)
          await leveling.remove_study_role(self, member)
     
  @commands.command(brief='Cập nhật lại role cho người dùng', description = "Hiển thị")
  async def update(self, ctx):
    #==================================================
    await ctx.send('Đang cập nhật lại rank người dùng...')
    members = ctx.guild.members
    levels = self.level_utils.get_levels()
    users = self.user_utils.get_users()
    for user in users:
      # print("Role Updating...")
      if user.semester_learning != 0:
        for member in members:
          member_roles = member.roles
          if member.id == user.user_id:
            # learn_time = user['learning_time']
            semester_time = user.semester_learning
            for i in range(len(levels)):
              #Get Current Time Level
              if semester_time >= levels[i].mark and semester_time < levels[i].end:
                if levels[i].id in [role.id for role in member_roles]:
                  pass
                  # return
                else:
                  new_role = get(member.guild.roles, id=levels[i].id)
                  await member.add_roles(new_role)
                  user.current_level = levels[i].order
                  #=====High Rank=======
                  if user.highest_rank < levels[i].order:
                    user.highest_rank = levels[i].order
                  #=======================
              elif levels[i].id in [role.id for role in member_roles]:
                #remove current role
                cur_role = get(member.guild.roles, id=levels[i].id)
                await member.remove_roles(cur_role)
        #Save datebase
        self.user_utils.update_user(user)
    await ctx.send('Đã cập nhật xong.')
            
            
def setup(bot):
  bot.add_cog(leveling(bot))
