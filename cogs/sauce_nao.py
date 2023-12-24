import os
import io
import enum
import requests
from PIL import Image
from discord.ext import commands
import discord


class ImageSource(enum.Enum):
    PIXIV = 5
    DANBOORU = 9
    GELBOORU = 25
    TWITTER = 41
    YANDERE = 12

class SauceNaoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.script_dir = os.path.dirname(__file__)
        self.image_path = os.path.join(self.script_dir, '../images')

    @commands.command()
    async def 출처(self, ctx):
        image_url = await self.get_image_url(ctx)
        if not image_url:
            return

        image_file = self.download_image(image_url, self.image_path)

        if not image_file:
            return

        refined_data = self.search_image_from_saucenao(ctx, image_file)
        embed = self.make_embed(refined_data, image_url)
        await ctx.send(embed=embed)
        self.delete_image(image_file)

    async def get_image_url(self, ctx):
        if not ctx.message.reference:
            await ctx.send("이 명령어는 답장에 사용해 주세요!")
            return
        original_message = await ctx.fetch_message(ctx.message.reference.message_id)

        if not original_message.attachments:
            await ctx.send("답장에 이미지가 없습니다!")
            return

        image_url = original_message.attachments[0].url
        return image_url

    def search_image_from_saucenao(self, ctx, image_file):
        api_key = "42218dd95c8802cc066b761aed6f1a90aa15e58e"
        response = self.search_image(image_file, api_key)

        if response is None:
            return None
        return self.refine_response(response)

    def download_image(self, image_url, image_path):
        try:
            response = requests.get(image_url)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            return None

        image_name = 'tmp.jpg'
        file_path = os.path.join(image_path, image_name)

        with open(file_path, 'wb') as file:
            file.write(response.content)
        return file_path

    def make_embed(self, refined_data, image_url):
        embed = discord.Embed(title="아리스는 이미지 검색을 시도했습니다!", color=0x60c7fb)
        if refined_data is None:
            embed.description = "아리스는 이미지 검색에 실패했습니다.."
            embed.set_thumbnail(url='https://i.imgur.com/RVRafku.jpeg')
        else:
            embed.description = "아리스가 출처를 찾아왔습니다!"
            embed.set_thumbnail(url='https://i.imgur.com/7lViSii.png')

            embed.add_field(name='작가', value=refined_data['Creator'], inline=False)
            embed.add_field(name='출처', value=refined_data['Source'], inline=False)
            embed.add_field(name='남은 횟수', value=refined_data['Remaining'], inline=False)
        embed.set_image(url=image_url)

        return embed

    def search_image(self, image_file, api_key, minsim='80'):
        api_url = 'https://saucenao.com/search.php'
        payload = {
            'output_type': '2',
            'numres': '1',
            'minsim': minsim,
            'api_key': api_key,
        }
        image_bytes = self.convert_image_to_bytes(image_file)
        files = {'file': ("image.jpg", image_bytes)}

        try:
            response = requests.post(api_url, files=files, data=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            return
        return response.json()

    def convert_image_to_bytes(self, image_file):
        with Image.open(image_file) as image:
            image = image.convert('RGB')
            with io.BytesIO() as image_data:
                image.save(image_data, format='JPEG')
                return image_data.getvalue()

    def refine_response(self, response):
        if response is None:
            return None
        results = response['results']
        results = [res for res in results if float(res['header']['similarity']) >= 80.0]
        idxs = [res['header']['index_id'] for res in results]
        refined_res = None
        if ImageSource.PIXIV.value in idxs:
            res = [res for res in results
                   if res['header']['index_id'] == ImageSource.PIXIV.value][0]
            refined_res = {
                'Remaining': response['header']['long_remaining'],
                'Type': 'Pixiv',
                'Creator': res['data']['member_name'],
                'Source': res['data']['ext_urls'][0]}
        elif ImageSource.DANBOORU.value in idxs or ImageSource.GELBOORU.value in idxs or ImageSource.YANDERE.value in idxs:
            res = [res for res in results
                   if res['header']['index_id'] == ImageSource.DANBOORU.value or
                   res['header']['index_id'] == ImageSource.GELBOORU.value or
                   res['header']['index_id'] == ImageSource.YANDERE.value][0]
            refined_res = {
                'Remaining': response['header']['long_remaining'],
                'Type': 'Danbooru',
                'Creator': res['data']['creator'],
                'Source': res['data']['source']}
            if refined_res['Source'].startswith('https://i.pximg.net'):
                pix_id = refined_res['Source'].split('/')[-1]
                refined_res['Source'] = f"https://www.pixiv.net/artworks/{pix_id}"
        elif ImageSource.TWITTER.value in idxs:
            ...
        return refined_res

    def delete_image(self, file_path):
        if os.path.exists(file_path):
            os.remove(file_path)


async def setup(bot):
    await bot.add_cog(SauceNaoCog(bot))
