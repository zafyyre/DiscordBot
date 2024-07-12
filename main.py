import discord
from app.bot import run_bot
from app.video_uploader import run_uploader

# Create a Discord client instance
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

if __name__ == "__main__":
    run_uploader(client)
    run_bot(client)
