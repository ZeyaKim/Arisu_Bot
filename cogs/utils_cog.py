import discord
from discord.ext import commands
import os
import random
import time


class UtilsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.script_dir = os.path.dirname(__file__)
        self.image_path = os.path.join(self.script_dir, '../images')
        self.games = {}

    @commands.command()
    async def 팀짜기 (self, ctx, team_num, *args):
        team_num = int(team_num)
        if len(args) <= 1:
            with open(self.image_path + '/crying.jpg', 'rb') as f:
                picture = discord.File(f)
                await ctx.send(file=picture)
                await ctx.send("선생님은 같이 놀 친구가 없습니까?")
                return
        elif team_num == 1:
            with open(self.image_path + '/angry.jpg', 'rb') as f:
                picture = discord.File(f)
                await ctx.send(file=picture)
                await ctx.send("팀을 짜는 의미가 없지 않습니까?")
                return
        elif len(args) % team_num != 0:
            with open(self.image_path + '/angry.jpg', 'rb') as f:
                picture = discord.File(f)
                await ctx.send(file=picture)
                await ctx.send("선생님은 나눗셈도 할 줄 모릅니까?")
                return
                
        random.seed(a=int(time.time()))
        args_list = list(args)
        random.shuffle(args_list)
        teams = [args_list[i::team_num] for i in range(team_num)]
        embed = discord.Embed(title="아리스가 팀을 나눠보겠습니다!", color=0x60c7fb)
        embed.description = "아리스가 완벽한 팀을 짜왔습니다!"
        embed.set_thumbnail(url='https://i.imgur.com/7lViSii.png')
        
        for i, team in enumerate(teams, start=1):
            embed.add_field(name=f"팀 {i}", value='\n'.join(team), inline=False)
        await ctx.send(embed=embed)
        
    @commands.command()
    async def 하면함(self, ctx, game):
        if game not in self.games:
            self.games[game] = []
        if ctx.author in self.games[game]:
            self.games[game].remove(ctx.author)
            if not self.games[game]:
                self.games.pop(game)
                await ctx.send(f"{game}하면 할 사람들이 없습니다..")
        else:
            self.games[game].append(ctx.author)
            player_mentions = [player.display_name for player in self.games[game]]
            embed = discord.Embed(title=f"{game}하면 한다는 사람들은 총 {len(self.games[game])}명 입니다!", color=0x60c7fb)
            embed.add_field(name="참가자", value='\n'.join(player_mentions), inline=False)
            await ctx.send(embed=embed)

    
    @commands.command()
    async def 안함(self, ctx, game):
        if game in self.games:
            self.games.pop(game)
            with open(self.image_path + '/crying.jpg', 'rb') as f:
                picture = discord.File(f)
                await ctx.send(file=picture)
                await ctx.send(f"{game}하면 할 사람들이 없습니다..")
    
    @commands.command()
    async def 뭐함(self, ctx):
        if len(self.games) == 0:
            with open(self.image_path + '/crying.jpg', 'rb') as f:
                picture = discord.File(f)
                await ctx.send(file=picture)
                await ctx.send("오늘은 할 게임이 없습니다..")
            return
        
        embed = discord.Embed(title="오늘 일정입니다!", color=0x60c7fb)
        embed.set_thumbnail(url='https://i.imgur.com/7lViSii.png')
        for game, players in self.games.items():
            player_display_names = [player.display_name for player in players]
            player_list = '\n'.join(player_display_names)  # 참가자 목록을 문자열로 변환
            embed.add_field(name=game, value=player_list, inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def 함(self, ctx, game):
        if game not in self.games or not self.games[game]:
            await ctx.send(f"{game}하면 할 사람들이 없습니다..")
            return

        players = self.games[game]
        player_mentions = [player.mention for player in players]
        await ctx.send(f"{game} ㄱㄱ" + ' '.join(player_mentions))

        
        

async def setup(bot):
    await bot.add_cog(UtilsCog(bot))
