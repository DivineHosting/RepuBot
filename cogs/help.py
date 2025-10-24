import discord
from discord.ext import commands
import config
from cogs.utils import Utils

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx):
        """Show all commands and info about RepuBot"""
        embed = Utils.make_embed(
            title="🤖 RepuBot Help Menu",
            description="Manage and track your server’s reputation system with RepuBot.\n\n"
                        "**Prefix:** `+`\n"
                        "Use `/` commands for admin actions."
        )

        embed.add_field(
            name="👤 Member Commands",
            value=(
                "`+vouch @user <reason>` — Submit a vouch request\n"
                "`+rep @user` — View approved vouches\n"
                "`+p` — View your own vouches\n"
                "`+leaderboard` — Show top users\n"
                "`+help` — Show this menu"
            ),
            inline=False
        )

        embed.add_field(
            name="⚙️ Admin Slash Commands",
            value=(
                "`/approve <vouch_id>` — Approve a pending vouch\n"
                "`/deny <vouch_id>` — Deny a pending vouch\n"
                "`/setlogchannel #channel` — Set the log channel\n"
                "`/clearvouch @user` — Remove all vouches for a user"
            ),
            inline=False
        )

        embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else discord.Embed.Empty)
        await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
