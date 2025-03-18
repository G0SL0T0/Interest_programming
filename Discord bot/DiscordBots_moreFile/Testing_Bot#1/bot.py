import disnake
from disnake.ext import commands
from config import TOKEN

# Настройки бота
intents = disnake.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Загрузка Cog'ов
bot.load_extension("cogs.moderation")
bot.load_extension("cogs.fun")
bot.load_extension("cogs.utilities")
bot.load_extension("cogs.music")
bot.load_extension("cogs.economy")

# Запуск бота
if __name__ == "__main__":
    bot.run(TOKEN)