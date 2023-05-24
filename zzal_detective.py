import discord
from discord.ext import commands

discord_bot_token = 'MTExMDg3NDg3NzAwNDYxMTYyNQ.GFLqhO.w8oE0msGkgl-LwZeIxC_JvVgi0sB5mHT2n0jq8'

bot = commands.Bot(command_prefix= '`')


@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

bot.run(discord_bot_token)