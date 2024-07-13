import discord
import os
from discord.ext import commands, tasks
from app.video_handler import get_latest_video, get_file_content_from_google_drive, delete_file_from_google_drive
from app.responses import handle_response
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
GOOGLE_DRIVE_FOLDER_ID = os.getenv('GOOGLE_DRIVE_FOLDER_ID')

# Debug: Print the environment variables
print(f"DISCORD_TOKEN: {DISCORD_TOKEN[:10]}...")  # Only print a part for security
print(f"CHANNEL_ID: {CHANNEL_ID}")
print(f"GOOGLE_DRIVE_FOLDER_ID: {GOOGLE_DRIVE_FOLDER_ID}")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    if not check_google_drive.is_running():
        check_google_drive.start()
    print(f'{bot.user} is online!')

@tasks.loop(seconds=10)  # Check Google Drive every 10 seconds
async def check_google_drive():
    print("Checking for new videos in Google Drive...")
    channel = bot.get_channel(CHANNEL_ID)
    if channel is None:
        print("Discord channel not found.")
        return

    latest_file = get_latest_video()
    if latest_file is None:
        print("No new videos found in Google Drive.")
        return

    file_content = get_file_content_from_google_drive(latest_file['id'])
    
    try:
        if file_content:
            file_content.seek(0)
            print(f"Uploading {latest_file['name']} to Discord channel {CHANNEL_ID}...")
            await channel.send(file=discord.File(fp=file_content, filename=latest_file['name']))
            print(f"Uploaded {latest_file['name']} to Discord.")
                
            delete_file_from_google_drive(latest_file['id'])
            print(f"Deleted file {latest_file['id']} from Google Drive.")
        else:
            print(f"Failed to read the file content.")
    except Exception as e:
        print(f"Error uploading file to Discord: {e}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Prevent bot from responding to itself

    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)

    print(f"{username} said: '{user_message}' in the '{channel}' channel.")

    if user_message.startswith("?!"):
        user_message = user_message[2:]  # Remove the first two characters
        await send_message(message, user_message, is_private=True)
    elif user_message.startswith("&"):
        user_message = user_message[1:]  # Remove the first character
        await send_message(message, user_message, is_private=False)

async def send_message(message, user_message, is_private):
    try:
        response = handle_response(user_message)
        
        print(f"Response: '{response}'")  # Debug statement
        if not response:
            response = "I couldn't process that command. Use '&help' for more information."
        if is_private:
            try:
                await message.author.send(response)
            except discord.Forbidden:
                await message.channel.send(f"{message.author.mention}, I couldn't send you a DM. Please enable DMs from server members.")
        else:
            await message.channel.send(response)
    except Exception as e:
        print(e)

def run_bot():
    print("Starting the bot...")
    bot.run(DISCORD_TOKEN)