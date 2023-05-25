import discord
from discord.ext import commands
import os

TOKEN = os.getenv("DISCORD_TOKEN")
print(f'token = {TOKEN}')

intents = discord.Intents.all() # 기본 Intents 모두 활성화
bot = commands.Bot(command_prefix='`', intents=intents)  # Intents 추가

imagePath = './images'

@bot.command()
async def 끄앙(ctx):
    with open(f'{imagePath}/cry.jpg', 'rb') as f:
        await ctx.send(file=f)
    await ctx.send('끄앙!')

bot.run(TOKEN)