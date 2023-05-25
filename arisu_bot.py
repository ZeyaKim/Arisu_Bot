import discord
from discord.ext import commands
import os

TOKEN = os.getenv("DISCORD_TOKEN")
print(f'token = {TOKEN}')

intents = discord.Intents.all() # 기본 Intents 모두 활성화
bot = commands.Bot(command_prefix='`', intents=intents)  # Intents 추가

@bot.command()
async def hello(ctx):
    print('hello?')
    await ctx.send('Hello!')

bot.run(TOKEN)