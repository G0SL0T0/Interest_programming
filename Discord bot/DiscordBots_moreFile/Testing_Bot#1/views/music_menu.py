import disnake
from disnake.ui import View, Button
from views.main_menu import MainMenu

class MusicMenu(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button(label="Воспроизвести", style=disnake.ButtonStyle.primary, custom_id="play"))
        self.add_item(Button(label="Остановить", style=disnake.ButtonStyle.danger, custom_id="stop"))
        self.add_item(Button(label="Пауза", style=disnake.ButtonStyle.secondary, custom_id="pause"))
        self.add_item(Button(label="Продолжить", style=disnake.ButtonStyle.secondary, custom_id="resume"))
        self.add_item(Button(label="Пропустить", style=disnake.ButtonStyle.secondary, custom_id="skip"))
        self.add_item(Button(label="Назад", style=disnake.ButtonStyle.secondary, custom_id="back"))

    async def interaction_check(self, interaction: disnake.Interaction):
        if interaction.data.custom_id == "back":
            await interaction.response.edit_message(view=MainMenu())
        else:
            await interaction.response.send_message(f"Вы выбрали: {interaction.data.custom_id}", ephemeral=True)