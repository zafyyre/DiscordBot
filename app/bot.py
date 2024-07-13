import discord
import os
from discord.ext import commands, tasks
from app.dropbox_handler import get_latest_video, get_file_content_from_dropbox, delete_from_dropbox
from app.responses import handle_response
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
DROPBOX_FOLDER_PATH = os.getenv('DROPBOX_FOLDER_PATH')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} is online!')
    check_dropbox.start()

@tasks.loop(seconds=10)  # Check Dropbox every 10 seconds
async def check_dropbox():
    print("Checking for new videos in Dropbox...")
    channel = bot.get_channel(CHANNEL_ID)
    if channel is None:
        print("Discord channel not found.")
        return

    latest_file = get_latest_video(DROPBOX_FOLDER_PATH)
    if latest_file is None:
        print("No new videos found in Dropbox.")
        return

    file_content = get_file_content_from_dropbox(latest_file)
    
    try:
        if file_content:
            file_content.seek(0)
            print(f"Uploading {latest_file.name} to Discord channel {CHANNEL_ID}...")
            await channel.send(file=discord.File(fp=file_content, filename=latest_file.name))
            print(f"Uploaded {latest_file.name} to Discord.")
                
            delete_from_dropbox(latest_file)
            print(f"Deleted file {latest_file.name} from Dropbox.")
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
        user_message = user_message[2:]
        await send_message(message, user_message, is_private=True)
    elif user_message.startswith("&"):
        user_message = user_message[1:]
        await send_message(message, user_message, is_private=False)

async def send_message(message, user_message, is_private):
    try:
        response = handle_response(user_message)
        
        print(f"Response: '{response}'")  # Debug statement
        if not response:
            response = "I couldn't process that command. Use '&help' for more information."
        if is_private:
            await message.author.send(response)
        else:
            await message.channel.send(response)
    except Exception as e:
        print(e)

def run_bot():
    print("Starting the bot...")
    bot.run(DISCORD_TOKEN)
