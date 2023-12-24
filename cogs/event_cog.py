import datetime
from discord.ext import commands, tasks
import discord
import pytz

korea = pytz.timezone('Asia/Seoul')

# If no tzinfo is given then UTC is assumed.
time = datetime.time(hour=22, minute=30, tzinfo=korea)

class EventCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.kose_time.start()

  def cog_unload(self):
    self.kose_time.cancel()

  @tasks.loop(time=time)
  async def kose_time(self):
    # Check if today is Friday (4) or Saturday (5)
    if datetime.datetime.now(korea).weekday() in [4, 5]:
      return
    channel = self.bot.get_channel(736308994733375599) 
    await channel.send("벌써 10시 반입니다! 리코세 선생님은 자러 가십시오!")

async def setup(bot):
  await bot.add_cog(EventCog(bot))