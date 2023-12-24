import os
import asyncio
from discord.ext import commands
import discord


class AudioCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.script_dir = os.path.dirname(__file__)
        self.audio_path = os.path.join(self.script_dir, '../audios')
        self.imagePath = os.path.join(self.script_dir, '../images')

    @commands.command()
    async def 빰파카밤(self, ctx):
        print('빰파카밤')
        if not await self.checkInVoiceChannel(ctx):
            await ctx.send('음성 채널에 접속한 상태에서 명령해 주세요!')
            return
        await self.connectChannel(ctx)

    async def checkInVoiceChannel(self, ctx):
        if ctx.author.voice and ctx.author.voice.channel:
            return True
        return False

    async def connectChannel(self, ctx):
        channel = ctx.author.voice.channel
        voice_client = await channel.connect()
        audio_source = self.get_audio_source()

        with open(self.imagePath + '/smile.jpg', 'rb') as f:
            picture = discord.File(f)
            await ctx.send(file=picture)
            await ctx.send('빰파카밤!')

        # Use the correct path to your audio file.
        voice_client.play(audio_source)
        while voice_client.is_playing():
            await asyncio.sleep(1)  # Wait for 10 seconds
        await voice_client.disconnect()

    def get_audio_source(self):
        return discord.FFmpegPCMAudio(
            executable="D:/Tools/ffmpeg-master-latest-win64-gpl-shared/ffmpeg-master-latest-win64-gpl-shared/bin/ffmpeg.exe",
            source=f"{self.audio_path}/bbampakabam.mp3")


async def setup(bot):
    await bot.add_cog(AudioCog(bot))
