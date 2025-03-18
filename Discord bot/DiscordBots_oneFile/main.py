import disnake
from disnake.ext import commands
from disnake.ui import Button, View
from disnake import FFmpegPCMAudio
import random
import requests
import youtube_dl


# Настройки бота
intents = disnake.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

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

# Меню модерации
class ModerationMenu(View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="Удалить сообщение", style=disnake.ButtonStyle.primary)
    async def delete_message_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.send_message("Функция удаления сообщения.", ephemeral=True)

    @disnake.ui.button(label="Выдать предупреждение", style=disnake.ButtonStyle.danger)
    async def warn_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.send_message("Функция выдачи предупреждения.", ephemeral=True)

# Меню развлечений
class FunMenu(View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="Случайное число", style=disnake.ButtonStyle.success)
    async def roll_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        number = random.randint(1, 100)
        await interaction.response.send_message(f"🎲 Выпало число: {number}", ephemeral=True)

    @disnake.ui.button(label="Мем", style=disnake.ButtonStyle.success)
    async def meme_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.send_message("Функция генерации мема.", ephemeral=True)

# Меню утилит
class UtilitiesMenu(View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="Погода", style=disnake.ButtonStyle.secondary)
    async def weather_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.send_message("Введите город для получения погоды.", ephemeral=True)

    @disnake.ui.button(label="Переводчик", style=disnake.ButtonStyle.secondary)
    async def translate_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.send_message("Функция перевода текста.", ephemeral=True)

# Меню музыки
class MusicMenu(View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="Воспроизвести", style=disnake.ButtonStyle.danger)
    async def play_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.send_message("Введите ссылку на YouTube для воспроизведения.", ephemeral=True)

    @disnake.ui.button(label="Остановить", style=disnake.ButtonStyle.danger)
    async def stop_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.send_message("Музыка остановлена.", ephemeral=True)
        
@bot.command()
async def quiz(ctx):
    questions = [
        {"question": "Сколько планет в Солнечной системе?", "answer": "8"},
        {"question": "Кто написал 'Войну и мир'?", "answer": "Толстой"},
    ]
    question = random.choice(questions)
    await ctx.send(f"Вопрос: {question['question']}")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for("message", timeout=10.0, check=check)
    except disnake.TimeoutError:
        await ctx.send("Время вышло!")
    else:
        if msg.content.lower() == question["answer"].lower():
            await ctx.send("Правильно!")
        else:
            await ctx.send(f"Неправильно! Правильный ответ: {question['answer']}")

@bot.command()
async def joke(ctx):
    jokes = [
        "Почему программисты путают Хэллоуин и Рождество? Потому что Oct 31 == Dec 25!",
        "Почему программисты не любят природу? Там слишком много багов.",
    ]
    await ctx.send(random.choice(jokes))
    
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: disnake.Member, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} был забанен.")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: disnake.Member, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} был кикнут.")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"Удалено {amount} сообщений.", delete_after=5)

@bot.command()
async def translate(ctx, text: str, lang: str):
    url = f"https://api.mymemory.translated.net/get?q={text}&langpair=en|{lang}"
    response = requests.get(url).json()
    translation = response["responseData"]["translatedText"]
    await ctx.send(f"Перевод: {translation}")
    
@bot.command()
async def play(ctx, url: str):
    voice_channel = ctx.author.voice.channel
    if not voice_channel:
        await ctx.send("Вы должны находиться в голосовом канале!")
        return

    voice_client = await voice_channel.connect()
    with ytdl as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        voice_client.play(FFmpegPCMAudio(url2))

@bot.command()
async def stop(ctx):
    voice_client = ctx.voice_client
    if voice_client.is_playing():
        voice_client.stop()
        await ctx.send("Музыка остановлена.")
        
@bot.command()
async def google(ctx, query: str):
    await ctx.send(f"Результаты поиска для '{query}': https://www.google.com/search?q={query}")
    
# Событие при запуске бота
@bot.event
async def on_ready():
    print(f"{bot.user.name}: Запущен!")

# Команда для вызова главного меню
@bot.command()
async def menu(ctx):
    await ctx.send("Выберите категорию:", view=MainMenu())

# Запуск бота
bot.run("=")