import discord
import os
from dotenv import load_dotenv
from app.responses import handle_response

load_dotenv()

async def send_message(message, user_message, is_private):
    try:
        response = handle_response(user_message)
        if is_private:
            await message.author.send(response)
        else:
            await message.channel.send(response)
    except Exception as e:
        print(e)

def run_bot(client):
    @client.event
    async def on_ready():
        print(f'{client.user} is online!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
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

    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    client.run(DISCORD_TOKEN)
