import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import config
from database import connect_to_mongo

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

# Initialize bot
bot = commands.Bot(command_prefix=config.PREFIX, intents=intents)
bot.remove_command("help")  # Using custom help command

# Connect MongoDB
db_client = connect_to_mongo()
db = db_client["RepuBot"]

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} | ID: {bot.user.id}")
    try:
        synced = await bot.tree.sync()
        print(f"🔧 Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"⚠️ Failed to sync slash commands: {e}")
    print("🤖 RepuBot is online and ready to build reputations!")

async def load_cogs():
    """Load all bot cogs."""
    await bot.add_cog(__import__('cogs.member', fromlist=['member']).Member(bot, db))
    await bot.add_cog(__import__('cogs.admin', fromlist=['admin']).Admin(bot, db))
    await bot.add_cog(__import__('cogs.utils', fromlist=['utils']).Utils(bot))
    await bot.add_cog(__import__('cogs.help', fromlist=['help']).Help(bot))

async def main():
    """Start bot asynchronously with all cogs loaded."""
    async with bot:
        await load_cogs()
        await bot.start(config.TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
