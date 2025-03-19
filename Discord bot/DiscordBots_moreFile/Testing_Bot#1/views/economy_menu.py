import disnake
from disnake.ui import View, Button
from views.main_menu import MainMenu

class EconomyMenu(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button(label="Баланс", style=disnake.ButtonStyle.primary, custom_id="balance"))
        self.add_item(Button(label="Ежедневный бонус", style=disnake.ButtonStyle.primary, custom_id="daily"))
        self.add_item(Button(label="Назад", style=disnake.ButtonStyle.secondary, custom_id="back"))

    async def interaction_check(self, interaction: disnake.Interaction):
        if interaction.data.custom_id == "back":
            await interaction.response.edit_message(view=MainMenu())
        else:
            await interaction.response.send_message(f"Вы выбрали: {interaction.data.custom_id}", ephemeral=True)