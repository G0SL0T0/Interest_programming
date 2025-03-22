import disnake
from disnake.ext import commands
from datetime import datetime, timezone
from views.main_menu import MainMenuView

class MainMenu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="menu", description="Главное меню")
    async def menu(self, interaction: disnake.ApplicationCommandInteraction):
        # Информация о пользователе
        member = interaction.author
        roles = [role.name for role in member.roles if role.name != "@everyone"]
        join_date = member.joined_at
        days_on_server = (datetime.now(timezone.utc) - join_date).days

        # Роли с эмодзи
        role_emojis = {
            "Маршал Банан": "🍌",
            "Прапорщик ананас": "🍍",
            "Старшина киви": "🥝",
            "Сержант Котэ": "🐱",
            "Сержант пиво": "🍺",
            "Младший сержант апельсин": "🍊",
            "Сержант баклажан": "🍆",
            "Рядовой Кокос": "🥥",
        }

        roles_with_emojis = [f"{role_emojis.get(role, '')} {role}" for role in roles]

        # Сообщение с информацией о пользователе
        embed_user = disnake.Embed(title=f"Статистика пользователя {member.display_name}", color=0x00ff00)
        embed_user.add_field(name="Роли", value="\n".join(roles_with_emojis), inline=False)
        embed_user.add_field(name="Время на сервере", value=f"{days_on_server} дней", inline=False)

        # Сообщение с информацией о боте и сервере
        embed_bot = disnake.Embed(title="Информация о боте и сервере", color=0x00ff00)
        embed_bot.add_field(name="Функционал бота", value="🎶 Музыка\n📊 Статистика\n🎮 Развлечения", inline=False)
        embed_bot.add_field(name="Сервер", value=f"Участников: {interaction.guild.member_count}", inline=False)

        # Отправляем сообщения
        await interaction.response.send_message(embed=embed_user)
        await interaction.followup.send(embed=embed_bot, view=MainMenuView(self.bot))

def setup(bot):
    bot.add_cog(MainMenu(bot))