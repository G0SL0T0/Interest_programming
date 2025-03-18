import disnake
from disnake.ui import View, Select

class MainMenu(View):
    def __init__(self):
        super().__init__(timeout=None)

        # Выпадающее меню для выбора категорий
        self.add_item(CategorySelect())

class CategorySelect(Select):
    def __init__(self):
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
            await interaction.response.edit_message(view=ModerationMenu())
        elif selected_category == "Развлечения":
            await interaction.response.edit_message(view=FunMenu())
        elif selected_category == "Утилиты":
            await interaction.response.edit_message(view=UtilitiesMenu())
        elif selected_category == "Музыка":
            await interaction.response.edit_message(view=MusicMenu())
        elif selected_category == "Экономика":
            await interaction.response.edit_message(view=EconomyMenu())