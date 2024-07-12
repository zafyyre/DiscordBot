import random
import json
import requests

def handle_response(message):
    input = message.lower()

<<<<<<< HEAD
    if input == "&":
        return "Type a valid command. Use '&help' for more information."
=======
    if input == "!":
        return "Type a valid command."
    
    elif input == "!help":
        return "\nThis shows how to use the bot. Type a command with '!<command>' to get started. To send a private message, type '?!<command>'.\t\nThese are the commands below:\n\t-'hello'\n\t-'roll'\n\t-'fact'\n\t-'compliment'"
>>>>>>> 04cac4e8fa750cada38bcf18a0be6f3c55b31354

    elif input == "&help":
        return "\nThis shows how to use the bot. Type a command with '&<command>' to get started.\nTo receive a private message, type '?!<command>'.\nThese are the commands below:\n\t-'hello'\n\t-'roll'\n\t-'fact'\n\t-'insult'\n\t'random'"

    elif input == "&hello":
        return "Hey there!"

    elif input == "&roll":
        return str(random.randint(1, 100))

    elif input == "&fact":
        url = "https://uselessfacts.jsph.pl/random.json?language=en"
        response = requests.get(url)
        data = response.json()
        return data["text"]

<<<<<<< HEAD
    elif input == f"&random":
        picks = random.choice(['agent1', 'agent2', 'agent3'])
        return picks
=======
        return data['text']
    
    elif input == "!compliment":
        insults = ["You're amazing", "You look good today!", "Nothing can stop you!"]
        return str(random.choice(insults))
>>>>>>> 04cac4e8fa750cada38bcf18a0be6f3c55b31354
