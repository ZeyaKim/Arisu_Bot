import discord
from discord.ext import commands
from discord import Embed
import os
import random


class TalkCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.script_dir = os.path.dirname(__file__)
        self.imagePath = os.path.join(self.script_dir, '../images')

    @commands.command()
    async def 끄앙(self, ctx):
        print('끄앙!')
        with open(self.imagePath + '/crying.jpg', 'rb') as f:
            picture = discord.File(f)
            await ctx.send(file=picture)
            await ctx.send('끄앙!')

    @commands.command()
    async def 깡통(self, ctx):
        print('아리스는 깡통이 아닙니다!')
        with open(self.imagePath + '/angry.jpg', 'rb') as f:
            picture = discord.File(f)
            await ctx.send(file=picture)
            await ctx.send('아리스는 깡통이 아닙니다!')

    @commands.command()
    async def 추천(self, ctx, *args):
        pick = random.choice(args)
        await ctx.send(f'아리스는 {pick}을(를) 추천합니다!')

    @commands.command()
    async def 주사위(self, ctx, start='1', end='100'):
        user = ctx.message.author
        userNickname = user.nick or user.name
        randNum = random.randint(int(start), int(end))
        await ctx.send(f'{userNickname} 선생님이 주사위를 굴려 {randNum} 이(가) 나왔습니다! ({start}-{end})')

    @commands.command()
    async def 선샌니(self, ctx):
        state_function_dict = {
            'sleeping': self.sleeping,
            'smoking': self.smoking,
            'burning': self.burning,
        }
        # 상태를 랜덤하게 선택
        random_state = random.choice(list(state_function_dict.keys()))

        # 선택된 상태에 따라 함수를 실행
        print(await state_function_dict[random_state](ctx))

    async def sleeping(self, ctx):
        with open(self.imagePath + '/sleeping.jpg', 'rb') as f:
            picture = discord.File(f)
            await ctx.send(file=picture)
            await ctx.send('불꺼조')

    async def smoking(self, ctx):
        with open(self.imagePath + '/smoking.jpg', 'rb') as f:
            picture = discord.File(f)
            await ctx.send(file=picture)
            await ctx.send('불ㅋ좀')

    async def burning(self, ctx):
        with open(self.imagePath + '/burning.gif', 'rb') as f:
            picture = discord.File(f)
            await ctx.send(file=picture)
            await ctx.send('불꺼조')

    @commands.command()
    async def 프사(self, ctx):
        user = ctx.author

        # Default avatar URL
        avatar_url = user.display_avatar.url

        embed = Embed(color=0x60c7fb)
        embed.set_image(url=avatar_url)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(TalkCog(bot))
