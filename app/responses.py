import random
import json
import requests
from app.valorant_agents import agents

def handle_response(message):
    input = message.lower()

    if input == "help":
        return "\nThis shows how to use the bot. Type a command with '&<command>' to get started.\nTo receive a private message, type '?!<command>'.\nThese are the commands below:\n\t-'hello'\n\t-'roll'\n\t-'fact'\n\t-'agent'"

    elif input == "hello":
        return "Hey there!"

    elif input == "roll":
        return str(random.randint(1, 100))

    elif input == "fact":
        url = "https://uselessfacts.jsph.pl/random.json?language=en"
        response = requests.get(url)
        data = response.json()
        return data["text"]

    elif input == "agent":
        picks = random.choice(agents)
        return picks
