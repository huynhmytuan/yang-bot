import discord
import datetime
from discord.ext import commands
from discord.utils import get
from helpers.custom_function import time_readable
import sys
sys.path.insert(1, '../')
from db.user_utils import UserUtils
from models.user import User
from db.level_utils import LevelUtils
from config import *

class tracking(commands.Cog):
  def __init__(self, bot):
    self.bot = bot  
    self.GUILD_ID = GUILD_ID
    self.guild = self.bot.get_guild(self.GUILD_ID)
    self.user_utils = UserUtils()
    self.level_utils = LevelUtils()

  @commands.command(brief='Bảng xếp hạng', aliases = ['t','lb'], description = "Hiển thị")
  async def top(self, ctx, top_type:str="semester"):
    users = self.user_utils.get_users()
    top_tuple = []
    top_title = ""
    value = ''
    #Sort Users by top learning time
    if top_type == "month":
      top_tuple = sorted(users, key = lambda User : User.month_learning, reverse=True)
      top_title = "BẢNG XẾP HẠNG THEO THÁNG"
      value = 'month_learning'
      
    elif top_type == "week":
      top_tuple = sorted(users, key = lambda User : User.week_learning, reverse=True)
      top_title = "BẢNG XẾP HẠNG THEO TUẦN"
      value = 'week_learning'

    elif top_type == "day":
      top_tuple = sorted(users, key = lambda User : User.day_learning, reverse=True)
      top_title = "BẢNG XẾP HẠNG THEO NGÀY"
      value = 'day_learning'

    elif top_type == "semester":
      top_tuple = sorted(users, key = lambda User : User.semester_learning, reverse=True)
      top_title = "BẢNG XẾP HẠNG THEO HỌC KÌ"
      value = 'semester_learning'
    elif top_type == "all":
      top_tuple = sorted(users, key = lambda User : User.learning_time , reverse=True)
      top_title = "BẢNG XẾP HẠNG TỔNG"
      value = 'learning_time'
    #Get index of requested user.
    list_result = []
    user_id = ctx.message.author.id
    index = -1
    for user in top_tuple:
      if user.user_id == user_id:
        index = top_tuple.index(user)
        break
    #Get 10 user around request user in leaderboard
    #get above user in top
    i = index
    count = 0
    limit = 5
    first_index = index
    # Num ofuser left
    if index == (len(users)-1):
      limit = 10
    while (i>=0) and (count!=limit):
      first_index = i
      i -= 1 
      count += 1
    user_left = 10 - count
    i = index
    count = 0
    last_index = index
    while( i != (len(users)-1) ) and (count != user_left):
      last_index = i
      i+=1
      count += 1
    for i in range(first_index, last_index):
      list_result.append(top_tuple[i])
    str_title = "Hạng".ljust(7)+"Số Giờ".ljust(10)+"Thành Viên"
    top_str = []
    for user in list_result:
      if user.user_id == user_id:
        str_user = ("#"+str(top_tuple.index(user)+1).ljust(7)+
        time_readable(user.getTime(value)).ljust(9)+
        str(self.bot.get_user(user.user_id).name))
        top_str.append(str_user)
      else:
        str_user = (" "+str(top_tuple.index(user)+1).ljust(7)+
        time_readable(user.getTime(value)).ljust(9)+
        str(self.bot.get_user(user.user_id).name))
        top_str.append(str_user)
    top = "\n".join(top_str)
    test1 = [str_title,top]
    text = "\n".join(test1)
    guide_txt = "Lệnh: -top <day|week|month|semester|all>\nGõ -help để xem tất cả các lệnh được hỗ trợ."
    embed = discord.Embed(color=0x002aff, timestamp = datetime.datetime.utcnow())
    embed.add_field(name=f"``` {top_title} ```", value=f"```CS\n{text}\n```\n{guide_txt}", inline=False)
    embed.set_footer(text=f'Người dùng {ctx.message.author.name}',icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed=embed)


  @commands.command(brief='Thời gian học của bạn', aliases = ["m"] )
  async def me(self, ctx):
    users_list = self.user_utils.get_users()
    #Get request member
    member = ctx.message.author
    for user in users_list:
      if member.id == user.user_id:
        #----------RANK--------
        #get top day
        rank_day = sorted(users_list, key = lambda User : User.day_learning, reverse=True)
        index_day = rank_day.index(user)
        #get top week
        rank_week = sorted(users_list, key = lambda User : User.week_learning , reverse=True)
        index_week = rank_week.index(user)
        #get top month
        rank_mon = sorted(users_list, key = lambda User : User.month_learning, reverse=True)
        index_mon = rank_mon.index(user)
        #get top semester
        rank_semes = sorted(users_list, key = lambda User : User.semester_learning, reverse=True)
        index_mon = rank_semes.index(user)
        #get top overall
        rank_total = sorted(users_list, key = lambda User : User.learning_time, reverse=True)
        index_total = rank_total.index(user)
        #======================
        str_title = ("Loại".ljust(10)+
        "Số Giờ".ljust(10)+
        "Thứ Hạng"+"\n")
        #Day
        str_day = str(
          "Ngày:".ljust(10)+
          time_readable(user.day_learning).ljust(10)+
          ("#"+str(index_day+1)))
        #week
        str_week = str("Tuần:".ljust(10)+
        time_readable(user.week_learning).ljust(10)+
        "#"+str(index_week+1))
        #Month
        str_mon = str("Tháng:".ljust(10)+
        time_readable(user.month_learning).ljust(10)+
        ("#"+str(index_mon+1)))
        #Semester
        str_semes = str("Học kì:".ljust(10)+
        time_readable(user.semester_learning).ljust(10)+
        ("#"+str(index_mon+1)))
        #day
        str_total = str("Tổng:".ljust(10)+
        time_readable(user.learning_time).ljust(10)+
        ("#"+str(index_total+1)))
        #==========
        value = [str_title, str_day, str_week, str_mon, str_semes, str_total]
        text = "\n".join(value)
        embed = discord.Embed(color=0x002aff, timestamp = datetime.datetime.utcnow())
        date_join = member.joined_at.strftime("%H:%M, Ngày %#d/%m/%Y")
        embed.add_field(name=f'``` BẢNG THỐNG KÊ CÁ NHÂN ```',value=f"\n**Thành Viên:** {member.mention}\n ```CS\n{text}\n\nNgày gia nhập: \n{date_join} ```\nGõ -help để xem tất cả các lệnh được hỗ trợ.",inline=False )
        embed.set_footer(text=f'Người dùng {member.name}',icon_url=member.avatar_url)
        await ctx.send(embed=embed)

  #=================================================
  @commands.command(brief='Thời gian học của bạn', aliases = ['personal',"p"])
  async def person(self, ctx):
    member = ctx.message.author
    levels = self.level_utils.get_levels()
    user = self.user_utils.get_user_by_id(member.id)
    uLv = user.current_level
    cur_level = None
    next_level = None
    role_rank = None
    high_rank = user.highest_rank
    hr = None
    #============High rank=========
    if high_rank == -1:
      hr = "Chưa có thành tích"
    #=================================
    if uLv == -1:
      cur_level = "Chưa Có Thành Tích"
      next_level = get(self.guild.roles, id=levels[0].id).mention
      role_rank = 0
      #=====Semester_learning Time
      method_semes = levels[0].end - user.semester_learning
      achive_semes = time_readable(method_semes)
    for i in range(len(levels)):
      #user have highest level
      if high_rank == levels[i].order:
        hr = get(self.guild.roles, id=levels[i].id).mention
      if uLv == levels[len(levels)-1].order:
        cur_level = get(self.guild.roles, id=levels[len(levels)-1].id).mention
        next_level = "Sắp Ra Mắt!"
        role_rank = len(levels)
        achive_semes = "Số giờ của bạn đã đạt tối đa"

      elif uLv == levels[i].order:
        cur_level = get(self.guild.roles, id=levels[i].id).mention
        next_level = get(self.guild.roles, id=levels[i+1].id).mention
        role_rank = levels[i].order+1
        #=====Semester_learning Time
        method_semes = levels[i].end - user.semester_learning
        achive_semes = time_readable(method_semes)

    embed = discord.Embed(title ="🌟BẢNG THÀNH TÍCH", color=member.color, timestamp = datetime.datetime.utcnow())
    embed.add_field(name="\u200b", value=f"*Thành tích được tính theo học kỳ (2 tháng)* \n **Thành tích hiện tại:** {cur_level}\n **Thành tích tiếp theo:** {next_level}\n\n ***Xếp hạng thành tích:***  ``👑{role_rank}/{len(levels)}``\n__Đạt thành tích tiếp theo còn cần__  ``⏰{achive_semes}``\n------------\n **Thành tích cao nhất đạt được:**\n  {hr} \n Gõ -help để xem tất cả các lệnh được hỗ trợ.",inline=False) 
    embed.set_footer(text=f'Người dùng {member.name}',icon_url=member.avatar_url)
    await ctx.send(embed=embed)

def setup(bot):
  bot.add_cog(tracking(bot))