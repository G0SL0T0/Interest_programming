import disnake
from disnake.ext import commands
from utils.economy import get_balance, update_balance, get_last_daily, set_last_daily
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

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
        last_daily = get_last_daily(user_id)
        if last_daily and (datetime.now() - last_daily).days < 1:
            await interaction.response.send_message("Вы уже получали бонус сегодня!", ephemeral=True)
            return

        update_balance(user_id, 100)
        set_last_daily(user_id, datetime.now())
        await interaction.response.send_message("Вы получили 100 монет!", ephemeral=True)

def setup(bot):
    bot.add_cog(Economy(bot))