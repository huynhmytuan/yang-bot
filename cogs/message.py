import discord
from discord.ext import commands
from discord.utils import get
from config import *
import datetime


class message(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.GUILD_ID = GUILD_ID
    self.ADMIN_CHANNEL_ID = ADMIN_CHANNEL_ID
    self.BOT_LOG_CHANNEL_ID = BOT_LOG_CHANNEL_ID
    self.GENARAL_CHAT_CHANNE_ID = GENARAL_CHAT_CHANNE_ID
  

  @commands.command(brief='Dùng để thông báo cho mọi người', aliases = ['sgc'])
  async def say_genaral_chat(self, ctx, *content : str) :
    if ctx.message.channel == self.bot.get_channel(self.ADMIN_CHANNEL_ID):
      # Get user message
      string = [char for char in content]
      text = " ".join(string)
      # Setup an emmbed
      embed = discord.Embed( title = "📌Note📌", color= 0x002aff, timestamp = datetime.datetime.utcnow())
      embed.add_field(name="\u200b", value=f"```{text}```",inline=False)
      embed.set_image(url = 'https://th.bing.com/th/id/R.7d8853669a238d9dbc1211c7e4bec321?rik=t%2bKciaQMtKJNBg&pid=ImgRaw&r=0')
       #Get bot log channel
      log_channel = self.bot.get_channel(self.GENARAL_CHAT_CHANNE_ID)   
         # Send emmbed to channel
      await log_channel.send(embed=embed)
      
def setup(bot):
  bot.add_cog(message(bot))