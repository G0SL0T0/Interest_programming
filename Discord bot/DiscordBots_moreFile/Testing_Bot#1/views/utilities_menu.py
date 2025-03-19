import disnake
from disnake.ui import View, Button
from views.main_menu import MainMenu

class UtilitiesMenu(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button(label="Погода", style=disnake.ButtonStyle.primary, custom_id="weather"))
        self.add_item(Button(label="Перевод", style=disnake.ButtonStyle.primary, custom_id="translate"))
        self.add_item(Button(label="Назад", style=disnake.ButtonStyle.secondary, custom_id="back"))

    async def interaction_check(self, interaction: disnake.Interaction):
        if interaction.data.custom_id == "back":
            await interaction.response.edit_message(view=MainMenu())
        else:
            await interaction.response.send_message(f"Вы выбрали: {interaction.data.custom_id}", ephemeral=True)