import disnake
from disnake.ext import commands
import youtube_dl
import logging
from config import TOKEN

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

bot.load_extension("cogs.main_menu")
bot.load_extension("cogs.moderation")
bot.load_extension("cogs.fun")
bot.load_extension("cogs.utilities")
bot.load_extension("cogs.music")
bot.load_extension("cogs.economy")

if __name__ == "__main__":
    bot.run(TOKEN)
