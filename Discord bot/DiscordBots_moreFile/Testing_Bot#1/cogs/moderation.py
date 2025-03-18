import disnake
from disnake.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="ban", description="Забанить участника")
    @commands.has_permissions(ban_members=True)
    async def ban(self, interaction: disnake.ApplicationCommandInteraction, member: disnake.Member, reason: str = None):
        await member.ban(reason=reason)
        await interaction.response.send_message(f"{member.mention} был забанен.")

    @commands.slash_command(name="kick", description="Кикнуть участника")
    @commands.has_permissions(kick_members=True)
    async def kick(self, interaction: disnake.ApplicationCommandInteraction, member: disnake.Member, reason: str = None):
        await member.kick(reason=reason)
        await interaction.response.send_message(f"{member.mention} был кикнут.")

    @commands.slash_command(name="clear", description="Очистить сообщения")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, interaction: disnake.ApplicationCommandInteraction, amount: int):
        await interaction.channel.purge(limit=amount + 1)
        await interaction.response.send_message(f"Удалено {amount} сообщений.", ephemeral=True)

def setup(bot):
    bot.add_cog(Moderation(bot))