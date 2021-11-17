import discord
from discord.ext import commands
from stay_alive import keep_alive
from helpers.scheduler_task import Run_Scheduler
import os
import time
from config import *

# Getting the information of new members
intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix="-", intents= intents)
bot.remove_command("help")

# -------------Get contants key--------------
TOKEN = os.getenv('TOKEN')
exten = ["cogs.leveling","cogs.tracking","cogs.statistic"]
# --------------Custom Help commands ---------------
@bot.group(invoke_without_command=True)
async def help(ctx):
  await ctx.channel.purge(limit=1)
  embed=discord.Embed(title="Help", description="Gõ -help <lệnh> để xem thêm thông tin mô tả chi tiết", color=0x00ada2)
  if ctx.message.channel.id == ADMIN_CHANNEL_ID:
    embed.add_field(name="-cd", value="Khởi tạo dữ liệu học cho toàn bộ người dùng.", inline=False)
    embed.add_field(name="-bk", value="Backup cơ sở dữ liệu.", inline=False)
    embed.add_field(name="-check", value="Kiểm tra bản sao lưu gần nhất.", inline=False)
    embed.add_field(name="-stats", value="Xuất bản thống kê theo xếp hạng", inline=False)
    embed.add_field(name="-end", value="Kết thúc học kì.", inline=False)
  else:
    embed.add_field(name="-me", value="Xem bảng thống kê cá nhân", inline=False)
    embed.add_field(name="-top", value="Xem bảng xếp hạng", inline=False)
    embed.add_field(name="-p", value="Xem bảng thành tích", inline=False)
  await ctx.send(embed=embed, delete_after=10)
@help.command()
async def me(ctx):
  embed=discord.Embed(title="Help: lệnh -me", description="Gõ lệnh **-me** (hoặc **-m**) để xem thống kê thành tích cá nhân của bạn. Bao gồm:\n\n+Thời gian học theo ngày, tuần, học kỳ, tháng và tất cả\n+Xếp hạng cá nhân cho từng hạng mục.", color=0x00ada2)
  await ctx.send(embed=embed)
@help.command()
async def top(ctx):
  embed=discord.Embed(title="Help: lệnh -top", description="Gõ lệnh **-top** (hoặc **-t** hoặc **-lb**) để xem bảng xếp hạng thành tích.\nMặc định bảng thành tích theo học kỳ sẽ được hiển thị.\n\n+ Xem xếp hạng theo ngày gõ: **-top day**\n+ Xem xếp hạng theo tuần gõ: **-top week**\n+ Xem xếp hạng theo tháng gõ: **-top month**\n+ Xem bảng xếp hạng học kỳ gõ: **-top semester**\n + Xem bảng xếp hạng tổng gõ: **-top all**", color=0x00ada2)
  await ctx.send(embed=embed)
@help.command()
async def p(ctx):
  embed=discord.Embed(title="Help: lệnh -p", description="Gõ lệnh **-p** (hoặc **-personal** hoặc **-person**) để xem bảng xếp hạng thành tích. Bao gồm hạng hiện tại, tiếp theo và số giờ còn thiếu để đạt thành tích tiếp theo.", color=0x00ada2)
  await ctx.send(embed=embed)

# dasdsd
os.environ['TZ'] = 'Asia/Ho_Chi_Minh'
time.tzset()
# --------------Connect Bot ---------------
@bot.event
async def on_ready():
  print('Bot đã sẵn sàng.')
  # -------Sync Extention-----
  for cog in exten:
     try:
       bot.load_extension(cog)
       print(f'{cog} was loaded!')
     except Exception as e:
       print('ERROR: '+str(e))
  Run_Scheduler()
  print('Running')
  
@bot.event
async def on_message(message):
  if (message.channel == bot.get_channel(ADMIN_CHANNEL_ID)) or (message.channel == bot.get_channel(LEARNING_STATS_CHANNEL_ID)) :
    if "Chào Yang" in message.content:
      await message.channel.send("Konichiwa, Yang desuuu! 🌸🌸 \nYang giúp mọi người đếm thời gian học đó, khen Yang đi hehe" )
    await bot.process_commands(message)


# -------Run Bot---------
keep_alive()
bot.run(TOKEN)