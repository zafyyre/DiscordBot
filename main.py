import discord
from app.bot import run_bot

# Create a Discord client instance
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

if __name__ == "__main__":
    run_bot()