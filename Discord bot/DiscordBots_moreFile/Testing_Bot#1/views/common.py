import disnake
from disnake.ui import Button
from views.main_menu import MainMenuView  # Ленивый импорт

class BackButton(Button):
    def __init__(self):
        super().__init__(label="Назад", style=disnake.ButtonStyle.secondary, custom_id="back")

    async def callback(self, interaction: disnake.Interaction):
        await interaction.response.edit_message(view=MainMenuView(self.view.bot))