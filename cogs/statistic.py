import discord
import datetime
from discord.ext import commands
from discord.utils import get
import time
from helpers.custom_function import time_readable
import sys
sys.path.insert(1, '../')
from db.user_utils import UserUtils
from models.user import User
from db.level_utils import LevelUtils
from config import *


class statistic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.GUILD_ID = GUILD_ID
        self.guild = self.bot.get_guild(self.GUILD_ID)
        self.ADMIN_CHANNEL_ID = ADMIN_CHANNEL_ID
        self.user_utils = UserUtils()
        self.level_utils = LevelUtils()

    @commands.command(brief='Xuất bảng xếp hạng theo yêu cầu.',
                      aliases=['s', 'st'],
                      description="Hiển thị")
    async def stats(self, ctx, top_type: str = "semester"):
        if ctx.message.channel == self.bot.get_channel(self.ADMIN_CHANNEL_ID):
            users = self.user_utils.get_users()
            top_tuple = []
            top_title = ""
            value = ''
            #Sort Users by top learning time
            if top_type == "month":
                top_tuple = sorted(users,
                                   key=lambda User: User.month_learning,
                                   reverse=True)
                now = datetime.datetime.now()
                top_title = f"TOP RANK - MONTH {now.month}\nCOUNT TO {now.strftime('%H:%M %d/%m/%Y')}"
                value = 'month_learning'
            elif top_type == "week":
                top_tuple = sorted(users,
                                   key=lambda User: User.week_learning,
                                   reverse=True)
                top_title = "WEEK RANKING"
                value = 'week_learning'
            elif top_type == "day":
                top_tuple = sorted(users,
                                   key=lambda User: User.day_learning,
                                   reverse=True)
                top_title = "DAY RANKING"
                value = 'day_learning'
            elif top_type == "semester":
                top_tuple = sorted(users,
                                   key=lambda User: User.semester_learning,
                                   reverse=True)
                now = datetime.datetime.now()
                top_title = f"SEMESTER RANKING\nCOUNT TO {now.strftime('%H:%M %d/%m/%Y')}"
                value = 'semester_learning'
            elif top_type == "all":
                top_tuple = sorted(users,
                                   key=lambda User: User.learning_time,
                                   reverse=True)
                top_title = "TOP RANK - ALL"
                value = 'learning_time'
            #Get index of requested user.
            str_title = "".ljust(20) + top_title + "\n" + "TOP RANK".ljust(
                13) + "TIME".ljust(8) + "USER".ljust(25) + "USER ID"
            top_str = [str_title]
            for user in top_tuple:
                str_user = (("_" * 80) + "\n" + "Top " +
                            str(top_tuple.index(user) + 1).ljust(10) +
                            (time_readable(user.getTime(value))).ljust(7) +
                            str(user.name).ljust(30) +
                            ("ID:" + str(user.user_id)))
                top_str.append(str_user)
            # test1 = [str_title, top_str]
            with open('top_result.txt', 'w') as txt:
                for element in top_str:
                    txt.write(element + "\n")
                txt.close()
            with open('top_result.txt', "rb") as file:
                await ctx.send("Đây là file thống kê của bạn nè nheee ",
                               file=discord.File(file, 'top_result.txt'))

    @commands.command(brief='Kết thúc học kì',
                      aliases=['e', 'end'],
                      description="Kết thúc một học kì và reset rank.")
    async def end_semester(self, ctx):
        await ctx.send('Thống Kê Kết Quả Học Tập Trong Học Kì...')
        time.sleep(3)
        await statistic.stats(self, ctx, "semester")
        await ctx.send(
            '**Đang tiến hành reset rank và thời gian học. Vui lòng đợi...**')
        if ctx.message.channel == self.bot.get_channel(self.ADMIN_CHANNEL_ID):
            members = self.guild.members
            levels = self.level_utils.get_levels()
            users = self.user_utils.get_users()
            time
            await statistic.backup(self, ctx)
            for user in users:
                if user.semester_learning != 0:
                    for member in members:
                        if member.id == user.user_id:
                            # member.
                            for role in levels:
                                if role.id in [r.id for r in member.roles]:
                                    # remove current role
                                    cur_role = get(member.guild.roles,
                                                   id=role.id)
                                    await member.remove_roles(cur_role)
                            user.semester_learning = 0
                            user.current_level = -1
                            break
            self.user_utils.upload_users(users)
        # Send respond message
        await ctx.send('**Đã Kết Thúc Một học Kì**')

    @commands.command(brief='Backup dữ liệu',
                      aliases=['b', 'bk'],
                      description="Backup dữ liệu")
    async def backup(self, ctx):
        if ctx.message.channel == self.bot.get_channel(self.ADMIN_CHANNEL_ID):
            users = self.user_utils.get_users()
            timestamp = time.time()
            self.user_utils.backup(users, timestamp)
            await ctx.send('Sao lưu dữ liệu thành công!')

    @commands.command(brief='Kiểm tra lần backup gần nhất',
                      aliases=['c', 'check'],
                      description="Kiểm tra lần backup gần nhất")
    async def check_backup(self, ctx):
        if ctx.message.channel == self.bot.get_channel(self.ADMIN_CHANNEL_ID):
            timestamp = int(self.user_utils.last_backup())
            backup_time = time.localtime(timestamp)
            format_time = time.strftime('%H:%M, Ngày %#d/%m/%Y', backup_time)
            await ctx.send(f'Lần sao lưu gần nhất:  {format_time}')

    @commands.command(brief='Khôi phục dữ liệu',
                      aliases=['back', 'rb'],
                      description="Khôi phục dữ liệu")
    async def roll_back(self, ctx):
        if ctx.message.channel == self.bot.get_channel(self.ADMIN_CHANNEL_ID):
              self.user_utils.roll_back()
              await ctx.send(
                  'Khôi phục dữ liệu thành công!\nKiến nghị sử dụng lệnh "-update" để cập nhật lại rank của người dùng.'
              )

def setup(bot):
    bot.add_cog(statistic(bot))
