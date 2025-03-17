import disnake
from disnake.ext import commands, tasks
from disnake.ui import Button, View, Select
import random
import json
import os
import requests
import youtube_dl
from disnake import FFmpegPCMAudio
from datetime import datetime, timedelta

# Настройки для youtube_dl
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

# Настройки бота
intents = disnake.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Экономика (сохранение данных)
if not os.path.exists("economy.json"):
    with open("economy.json", "w") as f:
        json.dump({}, f)

# Магазин ролей
roles_shop = {
    "Новобранец": {"price": 100, "emoji": "🟢"},
    "Рядовой": {"price": 300, "emoji": "🟡"},
    "Младший лейтенант": {"price": 600, "emoji": "🔵"},
    "Лейтенант": {"price": 1000, "emoji": "🔴"},
}

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

    @disnake.ui.button(label="Модерация", style=disnake.ButtonStyle.primary)
    async def moderation_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.edit_message(view=ModerationMenu())

    @disnake.ui.button(label="Развлечения", style=disnake.ButtonStyle.success)
    async def fun_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.edit_message(view=FunMenu())

    @disnake.ui.button(label="Утилиты", style=disnake.ButtonStyle.secondary)
    async def utilities_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.edit_message(view=UtilitiesMenu())

    @disnake.ui.button(label="Музыка", style=disnake.ButtonStyle.danger)
    async def music_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.edit_message(view=MusicMenu())

    @disnake.ui.button(label="Экономика", style=disnake.ButtonStyle.green)
    async def economy_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.edit_message(view=EconomyMenu())

# Меню модерации
class ModerationMenu(View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="Бан", style=disnake.ButtonStyle.danger)
    async def ban_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.send_modal(modal=BanModal())

    @disnake.ui.button(label="Кик", style=disnake.ButtonStyle.danger)
    async def kick_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.send_modal(modal=KickModal())

    @disnake.ui.button(label="Очистка", style=disnake.ButtonStyle.primary)
    async def clear_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.send_modal(modal=ClearModal())

    @disnake.ui.button(label="Назад", style=disnake.ButtonStyle.secondary)
    async def back_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.edit_message(view=MainMenu())

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

    @disnake.ui.button(label="Викторина", style=disnake.ButtonStyle.success)
    async def quiz_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        questions = [
            {"question": "Сколько планет в Солнечной системе?", "answer": "8"},
            {"question": "Кто написал 'Войну и мир'?", "answer": "Толстой"},
        ]
        question = random.choice(questions)
        await interaction.response.send_message(f"Вопрос: {question['question']}")

        def check(m):
            return m.author == interaction.author and m.channel == interaction.channel

        try:
            msg = await bot.wait_for("message", timeout=10.0, check=check)
        except disnake.TimeoutError:
            await interaction.followup.send("Время вышло!")
        else:
            if msg.content.lower() == question["answer"].lower():
                await interaction.followup.send("Правильно!")
            else:
                await interaction.followup.send(f"Неправильно! Правильный ответ: {question['answer']}")

    @disnake.ui.button(label="Шутка", style=disnake.ButtonStyle.success)
    async def joke_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        jokes = [
            "Почему программисты путают Хэллоуин и Рождество? Потому что Oct 31 == Dec 25!",
            "Почему программисты не любят природу? Там слишком много багов.",
        ]
        await interaction.response.send_message(random.choice(jokes))

    @disnake.ui.button(label="Забулить", style=disnake.ButtonStyle.success)
    async def zabul_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        games = [
            "🎲 Сыграем в кости?",
            "🎯 Сыграем в дартс?",
            "🃏 Сыграем в карты?",
            "🎮 Сыграем в игру?",
        ]
        game = random.choice(games)
        await interaction.response.send_message(f"{interaction.author.mention} {game}")

    @disnake.ui.button(label="Назад", style=disnake.ButtonStyle.secondary)
    async def back_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.edit_message(view=MainMenu())

# Меню утилит
class UtilitiesMenu(View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="Погода", style=disnake.ButtonStyle.secondary)
    async def weather_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.send_modal(modal=WeatherModal())

    @disnake.ui.button(label="Перевод", style=disnake.ButtonStyle.secondary)
    async def translate_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.send_modal(modal=TranslateModal())

    @disnake.ui.button(label="Назад", style=disnake.ButtonStyle.secondary)
    async def back_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.edit_message(view=MainMenu())

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
        api_key = "YOUR_OPENWEATHERMAP_API_KEY"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url).json()

        if response.get("cod") != 200:
            await interaction.response.send_message("Город не найден.", ephemeral=True)
            return

        weather_data = response["weather"][0]["description"]
        temperature = response["main"]["temp"]
        await interaction.response.send_message(f"Погода в {city}: {weather_data}, температура: {temperature}°C")

# Модальное окно для перевода
class TranslateModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Текст",
                placeholder="Укажите текст для перевода",
                custom_id="text",
                style=disnake.TextInputStyle.paragraph,
                max_length=500,
            ),
            disnake.ui.TextInput(
                label="Язык",
                placeholder="Укажите язык (например, 'ru')",
                custom_id="lang",
                style=disnake.TextInputStyle.short,
                max_length=10,
            ),
        ]
        super().__init__(title="Перевод", components=components, custom_id="translate_modal")

    async def callback(self, interaction: disnake.ModalInteraction):
        text = interaction.text_values["text"]
        lang = interaction.text_values["lang"]
        url = f"https://api.mymemory.translated.net/get?q={text}&langpair=en|{lang}"
        response = requests.get(url).json()
        translation = response["responseData"]["translatedText"]
        await interaction.response.send_message(f"Перевод: {translation}")

# Меню музыки
class MusicMenu(View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="Воспроизвести", style=disnake.ButtonStyle.danger)
    async def play_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.send_modal(modal=PlayModal())

    @disnake.ui.button(label="Остановить", style=disnake.ButtonStyle.danger)
    async def stop_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        voice_client = interaction.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
            await interaction.response.send_message("Музыка остановлена.", ephemeral=True)
        else:
            await interaction.response.send_message("Музыка не воспроизводится.", ephemeral=True)

    @disnake.ui.button(label="Назад", style=disnake.ButtonStyle.secondary)
    async def back_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.edit_message(view=MainMenu())

# Модальное окно для воспроизведения музыки
class PlayModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Ссылка",
                placeholder="Укажите ссылку на YouTube",
                custom_id="url",
                style=disnake.TextInputStyle.short,
                max_length=100,
            ),
        ]
        super().__init__(title="Воспроизвести музыку", components=components, custom_id="play_modal")

    async def callback(self, interaction: disnake.ModalInteraction):
        url = interaction.text_values["url"]
        voice_channel = interaction.author.voice.channel
        if not voice_channel:
            await interaction.response.send_message("Вы должны находиться в голосовом канале!", ephemeral=True)
            return

        voice_client = await voice_channel.connect()
        with youtube_dl.YoutubeDL(ytdl_format_options) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            voice_client.play(FFmpegPCMAudio(url2))
        await interaction.response.send_message("Музыка воспроизводится...")

# Меню экономики
class EconomyMenu(View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="Баланс", style=disnake.ButtonStyle.green)
    async def balance_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        user_id = str(interaction.author.id)
        balance = get_balance(user_id)
        await interaction.response.send_message(f"Ваш баланс: {balance} монет.", ephemeral=True)

    @disnake.ui.button(label="Ежедневный бонус", style=disnake.ButtonStyle.green)
    async def daily_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        user_id = str(interaction.author.id)
        update_balance(user_id, 100)
        await interaction.response.send_message("Вы получили 100 монет!", ephemeral=True)

    @disnake.ui.button(label="Магазин ролей", style=disnake.ButtonStyle.green)
    async def shop_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.edit_message(view=RoleShopMenu())

    @disnake.ui.button(label="Назад", style=disnake.ButtonStyle.secondary)
    async def back_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.edit_message(view=MainMenu())

# Магазин ролей
class RoleShopMenu(View):
    def __init__(self):
        super().__init__(timeout=None)

        # Выпадающее меню для выбора роли
        self.add_item(RoleSelect())

    @disnake.ui.button(label="Назад", style=disnake.ButtonStyle.secondary)
    async def back_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.edit_message(view=EconomyMenu())

# Выпадающее меню для выбора роли
class RoleSelect(disnake.ui.Select):
    def __init__(self):
        options = [
            disnake.SelectOption(label=role, description=f"Цена: {details['price']} монет", emoji=details["emoji"])
            for role, details in roles_shop.items()
        ]
        super().__init__(placeholder="Выберите роль", options=options, custom_id="role_select")

    async def callback(self, interaction: disnake.Interaction):
        selected_role = self.values[0]
        user = interaction.author
        user_roles = [role.name for role in user.roles]

        # Проверка, есть ли у пользователя более высокая роль
        if selected_role in user_roles:
            await interaction.response.send_message("У вас уже есть эта роль.", ephemeral=True)
            return

        # Проверка баланса
        price = roles_shop[selected_role]["price"]
        balance = get_balance(user.id)
        if balance < price:
            await interaction.response.send_message("Недостаточно монет.", ephemeral=True)
            return

        # Покупка роли
        update_balance(user.id, -price)
        role = disnake.utils.get(interaction.guild.roles, name=selected_role)
        await user.add_roles(role)
        await interaction.response.send_message(f"Вы купили роль {selected_role}!", ephemeral=True)

# Слэш-команда /menu
@bot.slash_command(name="menu", description="Открыть главное меню")
async def menu(interaction: disnake.ApplicationCommandInteraction):
    # Информация о пользователе
    user = interaction.author
    join_date = user.joined_at.strftime("%d.%m.%Y")
    roles = filter_roles(user.roles)
    balance = get_balance(user.id)

    user_info = (
        f"**Инфо {user.display_name}**\n"
        f"Время на сервере: {join_date}\n"
        f"Звание:\n"
        "{\n"
        + "\n".join([f"{role}" for role in roles]) +
        "\n}\n"
        f"**Баланс:** {balance} монет\n"
    )

    # Информация о боте
    bot_info = (
        f"🤖 **{bot.user.name}**\n"
        f"Сервер: {interaction.guild.name}\n"
        "**Функции бота:**\n"
        "- **Модерация**: Бан, кик, очистка сообщений.\n"
        "- **Развлечения**: Викторины, шутки, игры.\n"
        "- **Утилиты**: Погода, перевод.\n"
        "- **Музыка**: Воспроизведение треков.\n"
        "- **Экономика**: Виртуальная валюта, магазин ролей.\n"
    )

    # Отправка сообщения
    embed = disnake.Embed(title="Главное меню", color=disnake.Color.blue())
    embed.add_field(name="Информация о пользователе", value=user_info, inline=False)
    embed.add_field(name="Информация о боте", value=bot_info, inline=False)
    await interaction.response.send_message(embed=embed, view=MainMenu())

# Ежедневная награда за первое сообщение
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    user_id = str(message.author.id)
    today = datetime.now().strftime("%Y-%m-%d")

    # Проверка, получил ли пользователь награду сегодня
    with open("economy.json", "r") as f:
        economy = json.load(f)

    if economy.get(user_id, {}).get("last_message_date") != today:
        update_balance(user_id, 50)
        economy[user_id]["last_message_date"] = today
        with open("economy.json", "w") as f:
            json.dump(economy, f)
        await message.channel.send(f"{message.author.mention}, вы получили 50 монет за первое сообщение сегодня!")

    await bot.process_commands(message)

# Ежедневная награда за первую реакцию
@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    user_id = str(user.id)
    today = datetime.now().strftime("%Y-%m-%d")

    # Проверка, получил ли пользователь награду сегодня
    with open("economy.json", "r") as f:
        economy = json.load(f)

    if economy.get(user_id, {}).get("last_reaction_date") != today:
        update_balance(user_id, 30)
        economy[user_id]["last_reaction_date"] = today
        with open("economy.json", "w") as f:
            json.dump(economy, f)
        await reaction.message.channel.send(f"{user.mention}, вы получили 30 монет за первую реакцию сегодня!")

# Событие при запуске бота
@bot.event
async def on_ready():
    print(f"Бот {bot.user.name} готов к работе!")

# Запуск бота
bot.run("=")