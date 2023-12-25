import aiohttp
import asyncio
from discord.ext import commands
import discord
import os

class DanbooruCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_while_searching = False
        self.url = "https://danbooru.donmai.us/posts.json"

    async def download_file(self, session, url, file_name):
        async with session.get(url) as response:
            if response.status != 200:
                # 에러 처리
                print(f"Error downloading {url}: Status code {response.status}")
                return
            content = await response.read()
            self.write_file(file_name, content)

    def write_file(self, file_name, content):   
        with open(file_name, 'wb') as file:
            file.write(content)

    def make_params(self, tags, limit):
        params = {
            "tags": tags,
            "limit": limit
        }
        return params

    @commands.command()
    async def 짤(self, ctx):
        if self.is_while_searching:
            await ctx.send("다른 짤을 먼저 찾는 중입니다..")
            return
        self.is_while_searching = True
        try:
            params = self.make_params("", 200)
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url, params=params) as response:
                    if response.status != 200:
                        await ctx.send("아리스가 짤을 찾지 못했습니다...")
                        return
                    posts = await response.json()

                    posts = [post for post in posts if 'file_url' in post]
                    sorted_posts = sorted(posts, key=lambda post: post['score'], reverse=True)[:10]
                    url_list = [post['file_url'] for post in sorted_posts]
                    ext = [url.split('.')[-1] for url in url_list]
                    file_name_list = [f"SPOILER_image{idx}.{ext}" for idx, ext in enumerate(ext)]

                    download_tasks = [self.download_file(session, url, file_name) 
                                      for url, file_name in zip(url_list, file_name_list)]
                    await asyncio.gather(*download_tasks)

                    files = [discord.File(file_name, filename=file_name) for file_name in file_name_list]
                    await ctx.send("아리스가 짤을 모아왔습니다!", files=files)

                    for file_name in file_name_list:
                        os.remove(file_name)
        finally:
            self.is_while_searching = False

    @commands.command()
    async def 짤검색(self, ctx, *args):
        if len(args) >= 3:
            await ctx.send("3개 이상의 태그는 검색할 수 없습니다!")
            return

        if self.is_while_searching:
            await ctx.send("다른 짤을 먼저 찾는 중입니다..")
            return
        
        self.is_while_searching = True
        try:    
            tags = ' '.join(args)
            params = self.make_params(tags, 200)
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url, params=params) as response:
                    if response.status != 200:
                        await ctx.send("아리스가 짤을 찾지 못했습니다...")
                        return
                    posts = await response.json()

                    posts = [post for post in posts if 'file_url' in post]
                    sorted_posts = sorted(posts, key=lambda post: post['score'], reverse=True)[:10]
                    url_list = [post['file_url'] for post in sorted_posts]
                    ext = [url.split('.')[-1] for url in url_list]
                    file_name_list = [f"SPOILER_image{idx}.{ext}" for idx, ext in enumerate(ext)]

                    download_tasks = [self.download_file(session, url, file_name) 
                                      for url, file_name in zip(url_list, file_name_list)]
                    await asyncio.gather(*download_tasks)

                    files = [discord.File(file_name, filename=file_name) for file_name in file_name_list]
                    await ctx.send("아리스가 짤을 모아왔습니다!", files=files)

                    for file_name in file_name_list:
                        os.remove(file_name)
        except Exception as e:
            print(e)
            await ctx
