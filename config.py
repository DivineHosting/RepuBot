import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Secure values
TOKEN = os.getenv("DISCORD_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")

# Bot settings
PREFIX = "+"
BOT_NAME = "RepuBot"
EMBED_COLOR = 0x3498db
FOOTER_TEXT = "RepuBot • Building Reputation"
