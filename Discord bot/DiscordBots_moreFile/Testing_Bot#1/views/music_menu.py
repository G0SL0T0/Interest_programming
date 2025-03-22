import disnake
from disnake.ui import View, Button
from views.common import BackButton
from cogs.music import Music  # Ленивый импорт

class MusicMenu(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button(label="Воспроизвести", style=disnake.ButtonStyle.primary, custom_id="play"))
        self.add_item(Button(label="Остановить", style=disnake.ButtonStyle.danger, custom_id="stop"))
        self.add_item(Button(label="Пауза", style=disnake.ButtonStyle.secondary, custom_id="pause"))
        self.add_item(Button(label="Продолжить", style=disnake.ButtonStyle.secondary, custom_id="resume"))
        self.add_item(Button(label="Пропустить", style=disnake.ButtonStyle.secondary, custom_id="skip"))
        self.add_item(BackButton())

    async def interaction_check(self, interaction: disnake.Interaction):
        if interaction.data.custom_id == "back":
            await interaction.response.edit_message(view=MainMenuView())
        elif interaction.data.custom_id == "play":
            await interaction.response.send_modal(modal=AddTrackModal(self.bot))  # Открываем модальное окно для ввода ссылки
        elif interaction.data.custom_id == "stop":
            cog = Music(self.bot)  # Создаём экземпляр Music
            await cog.stop(interaction)  # Вызываем команду остановки
        elif interaction.data.custom_id == "pause":
            cog = Music(self.bot)  # Создаём экземпляр Music
            await cog.pause(interaction)  # Вызываем команду паузы
        elif interaction.data.custom_id == "resume":
            cog = Music(self.bot)  # Создаём экземпляр Music
            await cog.resume(interaction)  # Вызываем команду продолжения
        elif interaction.data.custom_id == "skip":
            cog = Music(self.bot)  # Создаём экземпляр Music
            await cog.skip(interaction)  # Вызываем команду пропуска