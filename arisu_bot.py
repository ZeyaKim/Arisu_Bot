import discord
from discord.ext import commands
import os


TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix= '`')


@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

bot.run(TOKEN)