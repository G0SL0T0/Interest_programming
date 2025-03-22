import disnake
import youtube_dl
from disnake.ext import commands
from config import TOKEN
import logging

# Настройка логов
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Настройки бота
intents = disnake.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Загрузка Cog'ов
bot.load_extension("cogs.main_menu")
bot.load_extension("cogs.moderation")
bot.load_extension("cogs.fun")
bot.load_extension("cogs.utilities")
bot.load_extension("cogs.music")
bot.load_extension("cogs.economy")

# Запуск бота
if __name__ == "__main__":
    bot.run(TOKEN)