import discord
from discord.ext import commands
import os

#TOKEN = os.getenv("DISCORD_TOKEN")
#print(f'token = {TOKEN}')

intents = discord.Intents.all() # 기본 Intents 모두 활성화
bot = commands.Bot(command_prefix='//', intents=intents)  # Intents 추가

cogs_path = './cogs'
folder = os.listdir(cogs_path)


@bot.event
async def on_ready():
    for ext in os.listdir(cogs_path):
        if ext.endswith(".py"):
            print(ext)
            await bot.load_extension(f'cogs.{ext.split(".")[0]}')


@bot.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send('빠밤빠밤! 아리스가 파티에 합류했습니다!')
            break


bot.run('MTExMDg3NDg3NzAwNDYxMTYyNQ.GYGZcN.VXUazqo0cCoREYylHRQGqngQV29oo--erKnm0c')