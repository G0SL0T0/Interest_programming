import disnake
from disnake.ext import commands, tasks
from disnake import FFmpegPCMAudio
import yt_dlp as youtube_dl
from config import ytdl_format_options
import logging
import asyncio

logger = logging.getLogger(__name__)

# Класс для интерактивного меню
class MusicControlView(disnake.ui.View):
    def __init__(self, voice_client, bot):
        super().__init__(timeout=None)
        self.voice_client = voice_client
        self.bot = bot
        self.update_view.start()

    @tasks.loop(seconds=5)
    async def update_view(self):
        # Проверяем, закончилось ли воспроизведение
        if not self.voice_client.is_playing() and not self.voice_client.is_paused():
            self.clear_items()  # Удаляем все кнопки
            self.add_item(disnake.ui.Button(label="Добавить трек", style=disnake.ButtonStyle.primary, custom_id="add_track"))
            await self.message.edit(view=self)
            self.update_view.stop()  # Останавливаем обновление
            return

        # Обновляем состояние кнопок и ползунка
        for child in self.children:
            if isinstance(child, disnake.ui.Button):
                if child.custom_id == "play_pause":
                    child.emoji = "⏸️" if self.voice_client.is_playing() else "▶️"
                elif child.custom_id == "stop":
                    child.disabled = not self.voice_client.is_playing()
                elif child.custom_id == "skip":
                    child.disabled = not self.voice_client.is_playing()
                elif child.custom_id == "progress":
                    # Обновляем текст ползунка
                    if self.voice_client.is_playing():
                        position = self.voice_client.position
                        duration = self.voice_client.source.duration
                        progress = int((position / duration) * 20)  # 20 символов для ползунка
                        child.label = "[" + "=" * progress + " " * (20 - progress) + "]"
                    else:
                        child.label = "[                    ]"

        # Обновляем сообщение с новым состоянием
        await self.message.edit(view=self)

    @disnake.ui.button(emoji="▶️", style=disnake.ButtonStyle.secondary, custom_id="play_pause")
    async def play_pause_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        if self.voice_client.is_playing():
            self.voice_client.pause()
            button.emoji = "▶️"
        else:
            self.voice_client.resume()
            button.emoji = "⏸️"
        await interaction.response.defer()

    @disnake.ui.button(emoji="⏹️", style=disnake.ButtonStyle.danger, custom_id="stop")
    async def stop_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        self.voice_client.stop()
        await interaction.response.defer()

    @disnake.ui.button(emoji="⏭️", style=disnake.ButtonStyle.secondary, custom_id="skip")
    async def skip_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        self.voice_client.stop()  # Останавливаем текущий трек
        await interaction.response.defer()

    @disnake.ui.button(emoji="🚪", style=disnake.ButtonStyle.danger, custom_id="leave")
    async def leave_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await self.voice_client.disconnect()
        await interaction.response.send_message("Бот вышел из канала.")
        self.update_view.stop()  # Останавливаем обновление меню

    @disnake.ui.button(label="Добавить трек", style=disnake.ButtonStyle.primary, custom_id="add_track")
    async def add_track_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.send_modal(modal=AddTrackModal(self.voice_client, self.bot))

    async def on_timeout(self):
        # Останавливаем обновление меню при истечении времени
        self.update_view.stop()

# Модальное окно для добавления трека
class AddTrackModal(disnake.ui.Modal):
    def __init__(self, voice_client, bot):
        super().__init__(title="Добавить трек", custom_id="add_track_modal")
        self.voice_client = voice_client
        self.bot = bot
        self.add_item(disnake.ui.TextInput(label="Ссылка на трек", custom_id="track_url", placeholder="Вставьте ссылку на YouTube..."))

    async def callback(self, interaction: disnake.Interaction):
        url = interaction.text_values["track_url"]
        await interaction.response.defer()

        try:
            with youtube_dl.YoutubeDL(ytdl_format_options) as ydl:
                info = ydl.extract_info(url, download=False)
                url2 = info['url']  # Используем 'url' вместо 'formats'
                self.voice_client.play(FFmpegPCMAudio(url2))

            # Отправляем новое интерактивное меню
            view = MusicControlView(self.voice_client, self.bot)
            await interaction.followup.send("Музыка воспроизводится...", view=view)
            view.message = await interaction.original_message()
        except Exception as e:
            logger.error(f"Ошибка при воспроизведении музыки: {e}")
            await interaction.followup.send(f"Произошла ошибка: {e}")

# Основной класс для музыки
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="play", description="Воспроизвести музыку")
    async def play(self, interaction: disnake.ApplicationCommandInteraction, url: str):
        await interaction.response.defer()  # Отложенный ответ, чтобы избежать тайм-аута

        # Проверка, что пользователь находится в голосовом канале
        if not interaction.author.voice:
            await interaction.followup.send("Вы должны находиться в голосовом канале!")
            return

        voice_channel = interaction.author.voice.channel
        voice_client = interaction.guild.voice_client

        # Проверка, что бот уже подключен к другому каналу
        if voice_client and voice_client.is_connected():
            if voice_client.channel != voice_channel:
                await interaction.followup.send("Бот уже подключен к другому каналу!")
                return
        else:
            # Подключение к голосовому каналу
            voice_client = await voice_channel.connect()

        try:
            # Извлечение информации о треке
            with youtube_dl.YoutubeDL(ytdl_format_options) as ydl:
                info = ydl.extract_info(url, download=False)
                url2 = info['url']  # Используем 'url' вместо 'formats'
                voice_client.play(FFmpegPCMAudio(url2))

            # Отправляем интерактивное меню
            view = MusicControlView(voice_client, self.bot)
            await interaction.followup.send("Музыка воспроизводится...", view=view)
            view.message = await interaction.original_message()
        except Exception as e:
            logger.error(f"Ошибка при воспроизведении музыки: {e}")
            await interaction.followup.send(f"Произошла ошибка: {e}")

def setup(bot):
    bot.add_cog(Music(bot))