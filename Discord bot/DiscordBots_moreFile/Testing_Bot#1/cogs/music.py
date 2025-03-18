import disnake
from disnake.ext import commands
import youtube_dl
from disnake import FFmpegPCMAudio
from config import ytdl_format_options

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="play", description="Воспроизвести музыку")
    async def play(self, interaction: disnake.ApplicationCommandInteraction, url: str):
        voice_channel = interaction.author.voice.channel
        if not voice_channel:
            await interaction.response.send_message("Вы должны находиться в голосовом канале!")
            return

        voice_client = await voice_channel.connect()
        with youtube_dl.YoutubeDL(ytdl_format_options) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            voice_client.play(FFmpegPCMAudio(url2))
        await interaction.response.send_message("Музыка воспроизводится...")

    @commands.slash_command(name="stop", description="Остановить музыку")
    async def stop(self, interaction: disnake.ApplicationCommandInteraction):
        voice_client = interaction.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
            await interaction.response.send_message("Музыка остановлена.")
        else:
            await interaction.response.send_message("Музыка не воспроизводится.")

def setup(bot):
    bot.add_cog(Music(bot))