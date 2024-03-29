from discord.ext import commands
import discord
import os
from PIL import Image, ImageSequence
import threading
import asyncio
import aiohttp
import io

class ImageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.script_dir = os.path.dirname(__file__)
        self.image_path = os.path.join(self.script_dir, '../images')
        self.loop = asyncio.get_event_loop() 
        if not os.path.exists(self.image_path):
            os.makedirs(self.image_path)

    @commands.command()
    async def 웹피(self, ctx):
        if not ctx.message.attachments:
            await ctx.send("움짤을 첨부해주세요!")
            return

        webp_files = [attachment for attachment in ctx.message.attachments if attachment.filename.endswith('.webp')]
        if not webp_files:
            await ctx.send("webp 파일을 첨부해주세요!")
            return

        for webp_file in webp_files:
            thread = threading.Thread(target=self.convert_webp_to_gif_thread, args=(ctx, webp_file,))
            thread.start()

    async def convert_webp_to_gif(self, ctx, webp_file):
        local_webp_path = os.path.join(self.image_path, webp_file.filename)
        await webp_file.save(local_webp_path)

        try:
            with Image.open(local_webp_path) as im:
                if not im.is_animated:
                    await ctx.send("움짤이 아닙니다!")
                    return None

                frames = [frame.copy() for frame in ImageSequence.Iterator(im)]

                # 이미지 모드가 "P"가 아닌 경우에만 변환
                if frames[0].mode != "P":
                    frames = [frame.convert("P") for frame in frames]

                local_gif_path = local_webp_path.replace('.webp', '.gif')
                frames[0].save(local_gif_path, save_all=True, append_images=frames[1:], loop=0)
                return local_gif_path
        except Exception as e:
            await ctx.send(f"움짤 변환 중 오류가 발생했습니다: {e}")
            if os.path.exists(local_webp_path):
                os.remove(local_webp_path)
            return None
        
    def convert_webp_to_gif_thread(self, ctx, webp_file):
        # 비동기 코루틴을 예약하고 결과를 기다립니다.
        future = asyncio.run_coroutine_threadsafe(self.convert_webp_to_gif(ctx, webp_file), self.loop)
        converted_gif = future.result()

        if converted_gif:
            asyncio.run_coroutine_threadsafe(self.send_converted_file(ctx, converted_gif), self.loop).result()
            # 변환 후 생성된 GIF 파일 삭제
            os.remove(converted_gif)
        # 원본 WebP 파일 삭제
        os.remove(os.path.join(self.image_path, webp_file.filename))

    async def send_converted_file(self, ctx, converted_gif):
        with open(converted_gif, 'rb') as f:
            picture = discord.File(f)
            try:
                await ctx.send(file=picture)
            except Exception as e:
                await ctx.send(f"파일 전송 중 오류가 발생했습니다: {e}")
                os.remove(converted_gif)

    @commands.command()
    async def 자르기(self, ctx, piece_count: int = 2):
        if not ctx.message.attachments:
            await ctx.send("이미지를 첨부해주세요!")
            return
        
        if len(ctx.message.attachments) > 1:
            await ctx.send("파일을 하나만 첨부해주세요!")
            return

        image_exts = ['.png', '.jpg', '.jpeg']
        
        if not ctx.message.attachments[0].filename.endswith(tuple(image_exts)):
            await ctx.send("이미지 파일을 첨부해주세요!")
            return
        
        image_file = ctx.message.attachments[0]
        
        async with aiohttp.ClientSession() as session:
            async with session.get(image_file.url) as response:
                if response.status != 200:
                    await ctx.send("이미지를 가져오지 못했습니다...")
                    return
                
                image_data = await response.read()
                
        image = Image.open(io.BytesIO(image_data))
        width, height = image.size
        base_slice_height = height // piece_count
        extra_pixels = width % piece_count

        os.makedirs('images/slice', exist_ok=True)

        sliced_images = []

        start_y = 0  # y축 시작점을 0으로 설정
        try:
            for i in range(piece_count):
                if i < extra_pixels:
                    slice_height = base_slice_height + 1
                else:
                    slice_height = base_slice_height

                end_y = start_y + slice_height  # 세로로 자르기 때문에, y축의 끝점을 조정
                slice = image.crop((0, start_y, width, end_y))  # x축은 전체, y축은 start_y부터 end_y까지

                slice_path = f'images/slice/slice_{i}.png'
                slice.save(slice_path)
                sliced_images.append(slice_path)

                start_y = end_y
                
            files = [discord.File(image_path, filename=image_path) for image_path in sliced_images]
            
            await ctx.send(f"{piece_count} 조각으로 자른 이미지들입니다!", files=files)
        finally:
            for image_path in sliced_images:
                if os.path.exists(image_path):
                    os.remove(image_path)

async def setup(bot):
    await bot.add_cog(ImageCog(bot))
