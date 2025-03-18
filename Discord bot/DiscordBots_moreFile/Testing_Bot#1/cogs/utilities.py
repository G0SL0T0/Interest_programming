import disnake
from disnake.ext import commands
import requests

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="weather", description="Получить погоду")
    async def weather(self, interaction: disnake.ApplicationCommandInteraction, city: str):
        api_key = "YOUR_OPENWEATHERMAP_API_KEY"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url).json()

        if response.get("cod") != 200:
            await interaction.response.send_message("Город не найден.")
            return

        weather_data = response["weather"][0]["description"]
        temperature = response["main"]["temp"]
        await interaction.response.send_message(f"Погода в {city}: {weather_data}, температура: {temperature}°C")

    @commands.slash_command(name="translate", description="Перевести текст")
    async def translate(self, interaction: disnake.ApplicationCommandInteraction, text: str, lang: str):
        url = f"https://api.mymemory.translated.net/get?q={text}&langpair=en|{lang}"
        response = requests.get(url).json()
        translation = response["responseData"]["translatedText"]
        await interaction.response.send_message(f"Перевод: {translation}")

def setup(bot):
    bot.add_cog(Utilities(bot))