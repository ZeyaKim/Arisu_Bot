import discord
from discord.ext import commands
import os
import io

TOKEN = os.getenv("DISCORD_TOKEN")
print(f'token = {TOKEN}')

intents = discord.Intents.all() # 기본 Intents 모두 활성화
bot = commands.Bot(command_prefix='`', intents=intents)  # Intents 추가

imagePath = './images'

@bot.command()
async def 끄앙(ctx):
    with open(os.path.join(imagePath, 'cry.jpg'), 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)
        await ctx.send('끄앙!')

bot.run(TOKEN)