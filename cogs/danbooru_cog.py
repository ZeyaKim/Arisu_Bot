import requests
import os
import asyncio
from discord.ext import commands
import discord


class DanbooruCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.proxies = {
            'http': 'http://103.191.155.46:8080',
            'https': 'http://103.191.155.46:8080',
        }

    async def download_file(self, url, file_name):
        response = requests.get(url)
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.write_file, file_name, response.content)

    def write_file(self, file_name, content):
        with open(file_name, 'wb') as file:
            file.write(content)

    @commands.command()
    async def 짤(self, ctx):
        url = "https://danbooru.donmai.us/posts.json"
        params = {
            "tags": "order:rank",
            "limit": 200
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            await ctx.send("아리스가 짤을 찾지 못했습니다...")
            return
        posts = response.json()

        sorted_posts = sorted(posts, key=lambda post: post['score'], reverse=True)[:10]
        url_list = [post['file_url'] for post in sorted_posts]
        extension = [url.split('.')[-1] for url in url_list]
        file_name_list = [f"SPOILER_image{idx}.{ext}" for idx, ext in enumerate(extension)]

        download_tasks = [self.download_file(url, file_name)
                          for url, file_name in zip(url_list, file_name_list)]
        await asyncio.gather(*download_tasks)

        files = [discord.File(file_name, filename=file_name) for file_name in file_name_list]
        await ctx.send("아리스가 짤을 모아왔습니다!", files=files)

        for file_name in file_name_list:
            os.remove(file_name)

    @commands.command()
    async def 짤검색(self, ctx):
        ...

async def setup(bot):
    await bot.add_cog(DanbooruCog(bot))
