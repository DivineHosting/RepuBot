import discord
from discord.ext import commands
import config

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def make_embed(title=None, description=None, color=config.EMBED_COLOR):
        embed = discord.Embed(title=title, description=description, color=color)
        embed.set_footer(text=config.FOOTER_TEXT)
        return embed
