import disnake
from disnake.ext import commands
from utils.economy import get_balance, update_balance

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="balance", description="Проверить баланс")
    async def balance(self, interaction: disnake.ApplicationCommandInteraction):
        user_id = str(interaction.author.id)
        balance = get_balance(user_id)
        await interaction.response.send_message(f"Ваш баланс: {balance} монет.", ephemeral=True)

    @commands.slash_command(name="daily", description="Получить ежедневный бонус")
    async def daily(self, interaction: disnake.ApplicationCommandInteraction):
        user_id = str(interaction.author.id)
        update_balance(user_id, 100)
        await interaction.response.send_message("Вы получили 100 монет!", ephemeral=True)

def setup(bot):
    bot.add_cog(Economy(bot))