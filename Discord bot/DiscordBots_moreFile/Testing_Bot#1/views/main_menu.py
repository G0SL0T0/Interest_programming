import disnake
from disnake.ui import View, Select

class MainMenuView(View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
        self.add_item(MainMenuSelect(self.bot))

class MainMenuSelect(Select):
    def __init__(self, bot):
        self.bot = bot
        options = [
            disnake.SelectOption(label="Модерация", description="Команды для модерации", emoji="🛡️"),
            disnake.SelectOption(label="Развлечения", description="Команды для развлечений", emoji="🎮"),
            disnake.SelectOption(label="Утилиты", description="Полезные команды", emoji="🔧"),
            disnake.SelectOption(label="Музыка", description="Команды для музыки", emoji="🎵"),
            disnake.SelectOption(label="Экономика", description="Команды для экономики", emoji="💰"),
        ]
        super().__init__(placeholder="Выберите категорию", options=options, custom_id="category_select")

    async def callback(self, interaction: disnake.Interaction):
        selected_category = self.values[0]
        if selected_category == "Модерация":
            from views.moderation_menu import ModerationMenu  # Ленивый импорт
            await interaction.response.edit_message(view=ModerationMenu(self.bot))
        elif selected_category == "Развлечения":
            from views.fun_menu import FunMenu  # Ленивый импорт
            await interaction.response.edit_message(view=FunMenu(self.bot))
        elif selected_category == "Утилиты":
            from views.utilities_menu import UtilitiesMenu  # Ленивый импорт
            await interaction.response.edit_message(view=UtilitiesMenu(self.bot))
        elif selected_category == "Музыка":
            from views.music_menu import MusicMenu  # Ленивый импорт
            await interaction.response.edit_message(view=MusicMenu(self.bot))
        elif selected_category == "Экономика":
            from views.economy_menu import EconomyMenu  # Ленивый импорт
            await interaction.response.edit_message(view=EconomyMenu(self.bot))