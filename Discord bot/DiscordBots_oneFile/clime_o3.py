import disnake
from disnake.ext import commands, tasks
from disnake.ui import View, Select
import json
import os
from datetime import datetime, timedelta

# Настройки бота
intents = disnake.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Экономика (сохранение данных)
if not os.path.exists("economy.json"):
    with open("economy.json", "w") as f:
        json.dump({}, f)

# Функция для получения баланса пользователя
def get_balance(user_id):
    with open("economy.json", "r") as f:
        economy = json.load(f)
    return economy.get(str(user_id), 0)

# Функция для обновления баланса
def update_balance(user_id, amount):
    with open("economy.json", "r") as f:
        economy = json.load(f)
    economy[str(user_id)] = economy.get(str(user_id), 0) + amount
    with open("economy.json", "w") as f:
        json.dump(economy, f)

# Функция для фильтрации ролей
def filter_roles(roles):
    filtered_roles = []
    for role in roles:
        if any(char in role.name for char in ["🍌", "🍍", "🥝", "🐱", "🍺", "🍊", "🍆", "🥥"]):
            filtered_roles.append(role.name)
    return filtered_roles

# Главное меню
class MainMenu(View):
    def __init__(self):
        super().__init__(timeout=None)

        # Выпадающее меню для выбора функций
        self.add_item(FunctionSelect())

# Выпадающее меню для выбора функций
class FunctionSelect(Select):
    def __init__(self):
        options = [
            disnake.SelectOption(label="Модерация", description="Функции модерации", emoji="🛠️"),
            disnake.SelectOption(label="Развлечения", description="Игры и шутки", emoji="🎮"),
            disnake.SelectOption(label="Утилиты", description="Погода, перевод", emoji="🔧"),
            disnake.SelectOption(label="Музыка", description="Воспроизведение музыки", emoji="🎵"),
            disnake.SelectOption(label="Экономика", description="Баланс и магазин", emoji="💰"),
        ]
        super().__init__(placeholder="Выберите функцию", options=options, custom_id="function_select")

    async def callback(self, interaction: disnake.Interaction):
        selected_function = self.values[0]
        if selected_function == "Модерация":
            await interaction.response.edit_message(view=ModerationMenu())
        elif selected_function == "Развлечения":
            await interaction.response.edit_message(view=FunMenu())
        elif selected_function == "Утилиты":
            await interaction.response.edit_message(view=UtilitiesMenu())
        elif selected_function == "Музыка":
            await interaction.response.edit_message(view=MusicMenu())
        elif selected_function == "Экономика":
            await interaction.response.edit_message(view=EconomyMenu())

# Меню модерации
class ModerationMenu(View):
    def __init__(self):
        super().__init__(timeout=None)

        # Выпадающее меню для выбора модерации
        self.add_item(ModerationSelect())

    @disnake.ui.button(label="Назад", style=disnake.ButtonStyle.secondary)
    async def back_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.edit_message(view=MainMenu())

# Выпадающее меню для выбора модерации
class ModerationSelect(Select):
    def __init__(self):
        options = [
            disnake.SelectOption(label="Бан", description="Забанить участника", emoji="🔨"),
            disnake.SelectOption(label="Кик", description="Кикнуть участника", emoji="👢"),
            disnake.SelectOption(label="Очистка", description="Очистить сообщения", emoji="🧹"),
        ]
        super().__init__(placeholder="Выберите действие", options=options, custom_id="moderation_select")

    async def callback(self, interaction: disnake.Interaction):
        selected_action = self.values[0]
        if selected_action == "Бан":
            await interaction.response.send_modal(modal=BanModal())
        elif selected_action == "Кик":
            await interaction.response.send_modal(modal=KickModal())
        elif selected_action == "Очистка":
            await interaction.response.send_modal(modal=ClearModal())

# Модальное окно для бана
class BanModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Участник",
                placeholder="Укажите @участника",
                custom_id="member",
                style=disnake.TextInputStyle.short,
                max_length=100,
            ),
            disnake.ui.TextInput(
                label="Причина",
                placeholder="Укажите причину",
                custom_id="reason",
                style=disnake.TextInputStyle.paragraph,
                required=False,
            ),
        ]
        super().__init__(title="Бан участника", components=components, custom_id="ban_modal")

    async def callback(self, interaction: disnake.ModalInteraction):
        member = interaction.text_values["member"]
        reason = interaction.text_values["reason"]
        await interaction.guild.ban(member, reason=reason)
        await interaction.response.send_message(f"{member} был забанен.", ephemeral=True)

# Модальное окно для кика
class KickModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Участник",
                placeholder="Укажите @участника",
                custom_id="member",
                style=disnake.TextInputStyle.short,
                max_length=100,
            ),
            disnake.ui.TextInput(
                label="Причина",
                placeholder="Укажите причину",
                custom_id="reason",
                style=disnake.TextInputStyle.paragraph,
                required=False,
            ),
        ]
        super().__init__(title="Кик участника", components=components, custom_id="kick_modal")

    async def callback(self, interaction: disnake.ModalInteraction):
        member = interaction.text_values["member"]
        reason = interaction.text_values["reason"]
        await interaction.guild.kick(member, reason=reason)
        await interaction.response.send_message(f"{member} был кикнут.", ephemeral=True)

# Модальное окно для очистки
class ClearModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Количество",
                placeholder="Укажите количество сообщений",
                custom_id="amount",
                style=disnake.TextInputStyle.short,
                max_length=10,
            ),
        ]
        super().__init__(title="Очистка сообщений", components=components, custom_id="clear_modal")

    async def callback(self, interaction: disnake.ModalInteraction):
        amount = int(interaction.text_values["amount"])
        await interaction.channel.purge(limit=amount + 1)
        await interaction.response.send_message(f"Удалено {amount} сообщений.", ephemeral=True)

# Меню развлечений
class FunMenu(View):
    def __init__(self):
        super().__init__(timeout=None)

        # Выпадающее меню для выбора развлечений
        self.add_item(FunSelect())

    @disnake.ui.button(label="Назад", style=disnake.ButtonStyle.secondary)
    async def back_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.edit_message(view=MainMenu())

# Выпадающее меню для выбора развлечений
class FunSelect(Select):
    def __init__(self):
        options = [
            disnake.SelectOption(label="Викторина", description="Сыграть в викторину", emoji="🎲"),
            disnake.SelectOption(label="Шутка", description="Получить шутку", emoji="😂"),
            disnake.SelectOption(label="Забулить", description="Предложить игру", emoji="🎮"),
        ]
        super().__init__(placeholder="Выберите развлечение", options=options, custom_id="fun_select")

    async def callback(self, interaction: disnake.Interaction):
        selected_fun = self.values[0]
        if selected_fun == "Викторина":
            await interaction.response.send_message("Викторина скоро будет добавлена!", ephemeral=True)
        elif selected_fun == "Шутка":
            jokes = [
                "Почему программисты путают Хэллоуин и Рождество? Потому что Oct 31 == Dec 25!",
                "Почему программисты не любят природу? Там слишком много багов.",
            ]
            await interaction.response.send_message(random.choice(jokes))
        elif selected_fun == "Забулить":
            games = [
                "🎲 Сыграем в кости?",
                "🎯 Сыграем в дартс?",
                "🃏 Сыграем в карты?",
                "🎮 Сыграем в игру?",
            ]
            game = random.choice(games)
            await interaction.response.send_message(f"{interaction.author.mention} {game}")

# Меню утилит
class UtilitiesMenu(View):
    def __init__(self):
        super().__init__(timeout=None)

        # Выпадающее меню для выбора утилит
        self.add_item(UtilitiesSelect())

    @disnake.ui.button(label="Назад", style=disnake.ButtonStyle.secondary)
    async def back_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.edit_message(view=MainMenu())

# Выпадающее меню для выбора утилит
class UtilitiesSelect(Select):
    def __init__(self):
        options = [
            disnake.SelectOption(label="Погода", description="Узнать погоду", emoji="🌤️"),
            disnake.SelectOption(label="Перевод", description="Перевести текст", emoji="🌍"),
        ]
        super().__init__(placeholder="Выберите утилиту", options=options, custom_id="utilities_select")

    async def callback(self, interaction: disnake.Interaction):
        selected_utility = self.values[0]
        if selected_utility == "Погода":
            await interaction.response.send_modal(modal=WeatherModal())
        elif selected_utility == "Перевод":
            await interaction.response.send_modal(modal=TranslateModal())

# Модальное окно для погоды
class WeatherModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Город",
                placeholder="Укажите город",
                custom_id="city",
                style=disnake.TextInputStyle.short,
                max_length=100,
            ),
        ]
        super().__init__(title="Погода", components=components, custom_id="weather_modal")

    async def callback(self, interaction: disnake.ModalInteraction):
        city = interaction.text_values["city"]
        api_key = ""
        url = 