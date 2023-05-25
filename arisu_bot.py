import discord
from discord.ext import commands
import os
import io

TOKEN = os.getenv("DISCORD_TOKEN")
print(f'token = {TOKEN}')

intents = discord.Intents.all() # 기본 Intents 모두 활성화
bot = commands.Bot(command_prefix='`', intents=intents)  # Intents 추가

imagePath = './images'


bot.run(TOKEN)