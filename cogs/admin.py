import discord
from discord.ext import commands
from discord import app_commands
from database import update_vouch_status, get_vouch_by_id, set_log_channel
from cogs.utils import Utils

class Admin(commands.Cog):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    @app_commands.command(name="approve", description="Approve a pending vouch by ID")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def approve(self, interaction: discord.Interaction, vouch_id: str):
        vouch = get_vouch_by_id(self.db, vouch_id)
        if not vouch:
            return await interaction.response.send_message("❌ Vouch not found.")

        update_vouch_status(self.db, vouch_id, "approved")
        embed = Utils.make_embed(
            title="✅ Vouch Approved",
            description=f"Approved vouch from <@{vouch['vouched_by']}> for <@{vouch['vouched_for']}>"
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="deny", description="Deny a pending vouch by ID")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def deny(self, interaction: discord.Interaction, vouch_id: str, reason: str = "No reason provided"):
        vouch = get_vouch_by_id(self.db, vouch_id)
        if not vouch:
            return await interaction.response.send_message("❌ Vouch not found.")

        update_vouch_status(self.db, vouch_id, "denied")
        embed = Utils.make_embed(
            title="🚫 Vouch Denied",
            description=f"Denied vouch from <@{vouch['vouched_by']}> for <@{vouch['vouched_for']}>\n**Reason:** {reason}"
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="setlogchannel", description="Set vouch-log channel for this server")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def setlogchannel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        set_log_channel(self.db, interaction.guild.id, channel.id)
        embed = Utils.make_embed(title="📢 Log Channel Set", description=f"All vouches will now be sent to {channel.mention}")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="clearvouch", description="Clear all vouches for a user")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def clearvouch(self, interaction: discord.Interaction, member: discord.Member):
        deleted = self.db.vouches.delete_many({"vouched_for": str(member.id), "guild_id": interaction.guild.id})
        embed = Utils.make_embed(title="🧹 Cleared Vouches", description=f"Removed `{deleted.deleted_count}` vouches for {member.mention}")
        await interaction.response.send_message(embed=embed)
