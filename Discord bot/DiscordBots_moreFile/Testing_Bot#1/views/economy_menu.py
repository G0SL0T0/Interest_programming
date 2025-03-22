import disnake
from disnake.ui import View, Button
from views.common import BackButton
from cogs.economy import Economy  # Ленивый импорт

class EconomyMenu(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button(label="Баланс", style=disnake.ButtonStyle.primary, custom_id="balance"))
        self.add_item(Button(label="Ежедневный бонус", style=disnake.ButtonStyle.primary, custom_id="daily"))
        self.add_item(BackButton())

    async def interaction_check(self, interaction: disnake.Interaction):
        if interaction.data.custom_id == "back":
            await interaction.response.edit_message(view=MainMenuView())
        elif interaction.data.custom_id == "balance":
            cog = Economy(self.bot)  # Создаём экземпляр Economy
            await cog.balance(interaction)  # Вызываем команду баланса
        elif interaction.data.custom_id == "daily":
            cog = Economy(self.bot)  # Создаём экземпляр Economy
            await cog.daily(interaction)  # Вызываем команду ежедневного бонуса