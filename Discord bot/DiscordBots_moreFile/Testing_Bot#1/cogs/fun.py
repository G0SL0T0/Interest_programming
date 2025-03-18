import disnake
from disnake.ext import commands
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="quiz", description="Начать викторину")
    async def quiz(self, interaction: disnake.ApplicationCommandInteraction):
        questions = [
            {"question": "Сколько планет в Солнечной системе?", "answer": "8"},
            {"question": "Кто написал 'Войну и мир'?", "answer": "Толстой"},
        ]
        question = random.choice(questions)
        await interaction.response.send_message(f"Вопрос: {question['question']}")

        def check(m):
            return m.author == interaction.author and m.channel == interaction.channel

        try:
            msg = await self.bot.wait_for("message", timeout=10.0, check=check)
        except disnake.TimeoutError:
            await interaction.followup.send("Время вышло!")
        else:
            if msg.content.lower() == question["answer"].lower():
                await interaction.followup.send("Правильно!")
            else:
                await interaction.followup.send(f"Неправильно! Правильный ответ: {question['answer']}")

    @commands.slash_command(name="joke", description="Получить шутку")
    async def joke(self, interaction: disnake.ApplicationCommandInteraction):
        jokes = [
            "Почему программисты путают Хэллоуин и Рождество? Потому что Oct 31 == Dec 25!",
            "Почему программисты не любят природу? Там слишком много багов.",
        ]
        await interaction.response.send_message(random.choice(jokes))

def setup(bot):
    bot.add_cog(Fun(bot))