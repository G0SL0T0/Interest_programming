import disnake
from disnake.ext import commands
from disnake.ui import Button, View
import random
import json
import os
import requests
import youtube_dl
from disnake import FFmpegPCMAudio

# Настройки бота
intents = disnake.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Экономика (сохранение данных)
if not os.path.exists("economy.json"):
    with open("economy.json", "w") as f:
        json.dump({}, f)

# Главное меню
class MainMenu(View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="Модерация", style=disnake.ButtonStyle.primary)
    async def moderation_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.send_message("Выберите действие:", view=ModerationMenu(), ephemeral=True)

    @disnake.ui.button(label="Развлечения", style=disnake.ButtonStyle.success)
    async def fun_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.send_message("Выберите действие:", view=FunMenu(), ephemeral=True)

    @disnake.ui.button(label="Утилиты", style=disnake.ButtonStyle.secondary)
    async def utilities_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.send_message("Выберите действие:", view=UtilitiesMenu(), ephemeral=True)

    @disnake.ui.button(label="Музыка", style=disnake.ButtonStyle.danger)
    async def music_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.send_message("Выберите действие:", view=MusicMenu(), ephemeral=True)

    @disnake.ui.button(label="Экономика", style=disnake.ButtonStyle.green)
    async def economy_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.send_message("Выберите действие:", view=EconomyMenu(), ephemeral=True)

# Меню модерации
class ModerationMenu(View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="Бан", style=disnake.ButtonStyle.danger)
    async def ban_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.send_message("Используйте команду `/ban @участник [причина]` для бана.", ephemeral=True)

    @disnake.ui.button(label="Кик", style=disnake.ButtonStyle.danger)
    async def kick_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.send_message("Используйте команду `/kick @участник [причина]` для кика.", ephemeral=True)

    @disnake.ui.button(label="Очистка", style=disnake.ButtonStyle.primary)
    async def clear_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.send_message("Используйте команду `/clear количество` для очистки сообщений.", ephemeral=True)

# Меню развлечений
class FunMenu(View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="Викторина", style=disnake.ButtonStyle.success)
    async def quiz_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.send_message("Используйте команду `/quiz` для начала викторины.", ephemeral=True)

    @disnake.ui.button(label="Шутка", style=disnake.ButtonStyle.success)
    async def joke_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.send_message("Используйте команду `/joke` для получения шутки.", ephemeral=True)

# Меню утилит
class UtilitiesMenu(View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="Погода", style=disnake.ButtonStyle.secondary)
    async def weather_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.send_message("Используйте команду `/weather город` для получения погоды.", ephemeral=True)

    @disnake.ui.button(label="Перевод", style=disnake.ButtonStyle.secondary)
    async def translate_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.send_message("Используйте команду `/translate текст язык` для перевода.", ephemeral=True)

# Меню музыки
class MusicMenu(View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="Воспроизвести", style=disnake.ButtonStyle.danger)
    async def play_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.send_message("Используйте команду `/play ссылка` для воспроизведения музыки.", ephemeral=True)

    @disnake.ui.button(label="Остановить", style=disnake.ButtonStyle.danger)
    async def stop_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.send_message("Используйте команду `/stop` для остановки музыки.", ephemeral=True)

# Меню экономики
class EconomyMenu(View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="Баланс", style=disnake.ButtonStyle.green)
    async def balance_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.send_message("Используйте команду `/balance` для проверки баланса.", ephemeral=True)

    @disnake.ui.button(label="Ежедневный бонус", style=disnake.ButtonStyle.green)
    async def daily_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.send_message("Используйте команду `/daily` для получения ежедневного бонуса.", ephemeral=True)

# Слэш-команда /menu
@bot.slash_command(name="menu", description="Открыть главное меню")
async def menu(interaction: disnake.ApplicationCommandInteraction):
    await interaction.response.send_message("Выберите категорию:", view=MainMenu())

# Модерация
@bot.slash_command(name="ban", description="Забанить участника")
@commands.has_permissions(ban_members=True)
async def ban(interaction: disnake.ApplicationCommandInteraction, member: disnake.Member, reason: str = None):
    await member.ban(reason=reason)
    await interaction.response.send_message(f"{member.mention} был забанен.")

@bot.slash_command(name="kick", description="Кикнуть участника")
@commands.has_permissions(kick_members=True)
async def kick(interaction: disnake.ApplicationCommandInteraction, member: disnake.Member, reason: str = None):
    await member.kick(reason=reason)
    await interaction.response.send_message(f"{member.mention} был кикнут.")

@bot.slash_command(name="clear", description="Очистить сообщения")
@commands.has_permissions(manage_messages=True)
async def clear(interaction: disnake.ApplicationCommandInteraction, amount: int):
    await interaction.channel.purge(limit=amount + 1)
    await interaction.response.send_message(f"Удалено {amount} сообщений.", delete_after=5)

# Развлечения
@bot.slash_command(name="quiz", description="Начать викторину")
async def quiz(interaction: disnake.ApplicationCommandInteraction):
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

@bot.slash_command(name="joke", description="Получить шутку")
async def joke(interaction: disnake.ApplicationCommandInteraction):
    jokes = [
        "Почему программисты путают Хэллоуин и Рождество? Потому что Oct 31 == Dec 25!",
        "Почему программисты не любят природу? Там слишком много багов.",
    ]
    await interaction.response.send_message(random.choice(jokes))

# Утилиты
@bot.slash_command(name="weather", description="Получить погоду")
async def weather(interaction: disnake.ApplicationCommandInteraction, city: str):
    api_key = "YOUR_OPENWEATHERMAP_API_KEY"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()

    if response.get("cod") != 200:
        await interaction.response.send_message("Город не найден.")
        return

    weather_data = response["weather"][0]["description"]
    temperature = response["main"]["temp"]
    await interaction.response.send_message(f"Погода в {city}: {weather_data}, температура: {temperature}°C")

@bot.slash_command(name="translate", description="Перевести текст")
async def translate(interaction: disnake.ApplicationCommandInteraction, text: str, lang: str):
    url = f"https://api.mymemory.translated.net/get?q={text}&langpair=en|{lang}"
    response = requests.get(url).json()
    translation = response["responseData"]["translatedText"]
    await interaction.response.send_message(f"Перевод: {translation}")

# Музыка
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

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

@bot.slash_command(name="play", description="Воспроизвести музыку")
async def play(interaction: disnake.ApplicationCommandInteraction, url: str):
    voice_channel = interaction.author.voice.channel
    if not voice_channel:
        await interaction.response.send_message("Вы должны находиться в голосовом канале!")
        return

    voice_client = await voice_channel.connect()
    with ytdl as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        voice_client.play(FFmpegPCMAudio(url2))
    await interaction.response.send_message("Музыка воспроизводится...")

@bot.slash_command(name="stop", description="Остановить музыку")
async def stop(interaction: disnake.ApplicationCommandInteraction):
    voice_client = interaction.guild.voice_client
    if voice_client.is_playing():
        voice_client.stop()
        await interaction.response.send_message("Музыка остановлена.")
    else:
        await interaction.response.send_message("Музыка не воспроизводится.")

# Экономика
@bot.slash_command(name="balance", description="Проверить баланс")
async def balance(interaction: disnake.ApplicationCommandInteraction):
    user_id = str(interaction.author.id)
    with open("economy.json", "r") as f:
        economy = json.load(f)
    balance = economy.get(user_id, 0)
    await interaction.response.send_message(f"Ваш баланс: {balance} монет.")

@bot.slash_command(name="daily", description="Получить ежедневный бонус")
async def daily(interaction: disnake.ApplicationCommandInteraction):
    user_id = str(interaction.author.id)
    with open("economy.json", "r") as f:
        economy = json.load(f)
    economy[user_id] = economy.get(user_id, 0) + 100
    with open("economy.json", "w") as f:
        json.dump(economy, f)
    await interaction.response.send_message("Вы получили 100 монет!")

# Событие при запуске бота
@bot.event
async def on_ready():
    print(f"Бот {bot.user.name} готов к работе!")

# Запуск бота
bot.run("=")