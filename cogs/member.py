import discord
from discord.ext import commands
from database import add_vouch, get_user_vouches, get_top_users, get_log_channel
from cogs.utils import Utils

class Member(commands.Cog):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    @commands.command(name="vouch")
    async def vouch(self, ctx, member: discord.Member, *, reason: str = None):
        """Submit a vouch for another user"""
        if not reason:
            return await ctx.reply("❌ Please provide a reason for your vouch.")

        if member.id == ctx.author.id:
            return await ctx.reply("⚠️ You cannot vouch for yourself!")

        vouch_id = add_vouch(self.db, ctx.guild.id, str(ctx.author.id), str(member.id), reason)
        embed = Utils.make_embed(
            title="📝 New Vouch Submitted",
            description=f"**From:** {ctx.author.mention}\n**For:** {member.mention}\n**Reason:** {reason}\n\n🆔 Vouch ID: `{vouch_id}`\n\nWaiting for admin approval."
        )
        await ctx.reply(embed=embed)

        # Send to vouch-log if configured
        log_channel_id = get_log_channel(self.db, ctx.guild.id)
        if log_channel_id:
            log_channel = ctx.guild.get_channel(log_channel_id)
            if log_channel:
                await log_channel.send(embed=embed)

    @commands.command(name="rep")
    async def rep(self, ctx, member: discord.Member = None):
        """View approved vouches for a user"""
        member = member or ctx.author
        vouches = get_user_vouches(self.db, str(member.id), ctx.guild.id)
        count = len(vouches)
        embed = Utils.make_embed(
            title=f"🌟 Reputation for {member.display_name}",
            description=f"✅ **Total Approved Vouches:** {count}"
        )
        await ctx.reply(embed=embed)

    @commands.command(name="p")
    async def my_vouches(self, ctx):
        """View your submitted vouches"""
        vouches = list(self.db.vouches.find({"vouched_by": str(ctx.author.id), "guild_id": ctx.guild.id}))
        if not vouches:
            return await ctx.reply("😕 You haven’t vouched for anyone yet.")
        desc = "\n".join(
            [f"🆔 `{v['_id']}` → <@{v['vouched_for']}> — **{v['status'].upper()}**"
             for v in vouches[:10]]
        )
        embed = Utils.make_embed(title=f"📜 Your Vouches", description=desc)
        await ctx.reply(embed=embed)

    @commands.command(name="leaderboard")
    async def leaderboard(self, ctx):
        """Show top users by vouches"""
        top_users = get_top_users(self.db, ctx.guild.id)
        if not top_users:
            return await ctx.reply("No vouches yet!")
        desc = ""
        for i, user in enumerate(top_users, start=1):
            u = ctx.guild.get_member(int(user["_id"]))
            name = u.display_name if u else f"User {user['_id']}"
            desc += f"**{i}.** {name} — {user['count']} vouches\n"
        embed = Utils.make_embed(title="🏆 Top Repu Users", description=desc)
        await ctx.reply(embed=embed)
