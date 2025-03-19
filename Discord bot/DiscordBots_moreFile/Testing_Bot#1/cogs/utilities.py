import disnake
from disnake.ext import commands
import requests
import logging

logger = logging.getLogger(__name__)

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="weather", description="Получить погоду")
    async def weather(self, interaction: disnake.ApplicationCommandInteraction, city: str):
        api_key = "YOUR_OPENWEATHERMAP_API_KEY"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        try:
            response = requests.get(url).json()
            if response.get("cod") != 200:
                await interaction.response.send_message("Город не найден.")
                return

            weather_data = response["weather"][0]["description"]
            temperature = response["main"]["temp"]
            embed = disnake.Embed(title=f"Погода в {city}", description=f"{weather_data}", color=0x00ff00)
            embed.add_field(name="Температура", value=f"{temperature}°C")
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            logger.error(f"Ошибка при запросе погоды: {e}")
            await interaction.response.send_message(f"Произошла ошибка: {e}")

    @commands.slash_command(name="translate", description="Перевести текст")
    async def translate(self, interaction: disnake.ApplicationCommandInteraction, text: str, lang: str):
        url = f"https://api.mymemory.translated.net/get?q={text}&langpair=en|{lang}"
        try:
            response = requests.get(url).json()
            translation = response["responseData"]["translatedText"]
            await interaction.response.send_message(f"Перевод: {translation}")
        except Exception as e:
            logger.error(f"Ошибка при переводе текста: {e}")
            await interaction.response.send_message(f"Произошла ошибка: {e}")

def setup(bot):
    bot.add_cog(Utilities(bot))