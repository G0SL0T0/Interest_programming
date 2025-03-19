import disnake
from disnake.ext import commands
import youtube_dl
from disnake import FFmpegPCMAudio
from config import ytdl_format_options
import logging

logger = logging.getLogger(__name__)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="play", description="Воспроизвести музыку")
    async def play(self, interaction: disnake.ApplicationCommandInteraction, url: str):
        if not interaction.author.voice:
            await interaction.response.send_message("Вы должны находиться в голосовом канале!")
            return

        voice_channel = interaction.author.voice.channel
        voice_client = interaction.guild.voice_client

        if voice_client and voice_client.is_connected():
            if voice_client.channel != voice_channel:
                await interaction.response.send_message("Бот уже подключен к другому каналу!")
                return
        else:
            voice_client = await voice_channel.connect()

        try:
            with youtube_dl.YoutubeDL(ytdl_format_options) as ydl:
                info = ydl.extract_info(url, download=False)
                url2 = info['formats'][0]['url']
                voice_client.play(FFmpegPCMAudio(url2))
            await interaction.response.send_message("Музыка воспроизводится...")
        except Exception as e:
            logger.error(f"Ошибка при воспроизведении музыки: {e}")
            await interaction.response.send_message(f"Произошла ошибка: {e}")

    @commands.slash_command(name="stop", description="Остановить музыку")
    async def stop(self, interaction: disnake.ApplicationCommandInteraction):
        voice_client = interaction.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
            await interaction.response.send_message("Музыка остановлена.")
        else:
            await interaction.response.send_message("Музыка не воспроизводится.")

    @commands.slash_command(name="pause", description="Приостановить музыку")
    async def pause(self, interaction: disnake.ApplicationCommandInteraction):
        voice_client = interaction.guild.voice_client
        if voice_client.is_playing():
            voice_client.pause()
            await interaction.response.send_message("Музыка приостановлена.")
        else:
            await interaction.response.send_message("Музыка не воспроизводится.")

    @commands.slash_command(name="resume", description="Возобновить музыку")
    async def resume(self, interaction: disnake.ApplicationCommandInteraction):
        voice_client = interaction.guild.voice_client
        if voice_client.is_paused():
            voice_client.resume()
            await interaction.response.send_message("Музыка возобновлена.")
        else:
            await interaction.response.send_message("Музыка не приостановлена.")

    @commands.slash_command(name="skip", description="Пропустить текущий трек")
    async def skip(self, interaction: disnake.ApplicationCommandInteraction):
        voice_client = interaction.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
            await interaction.response.send_message("Трек пропущен.")
        else:
            await interaction.response.send_message("Музыка не воспроизводится.")

def setup(bot):
    bot.add_cog(Music(bot))