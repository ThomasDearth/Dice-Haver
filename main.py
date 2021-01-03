# bot.py
import os
import discord
from dotenv import load_dotenv
import command_modules.roll

print("1")

# Imports Discord token without having it hardcoded into the program
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

# Removes duplicate spaces from a message and converts it to lowercase
def clean(message):
    message = message.lower()
    message = " ".join(message.split())
    return message

# Returns documentation as a message in the channel
def help_message(message_content, message_author):
    return "@" + str(message_author)[:len(str(message_author))-5] + " Hi! I'm a dice-rolling bot for your discord servers!\nBasic commands:\n`!help`\tdisplays this page\n`!github`\tPosts a link to the GitHub page where the source code is posted\n\nSimple dice rolls:\n`!roll N`\t rolls *N* six-sided dice\n`!roll dN`\t rolls one die with *N* sides\n`!roll XdY`\t rolls *X* dice with *Y* sides each\n\nSoulbound-specific tools:\n`!roll [dice] tX`\tSpecifies the target number (x) a die must meet\n`!roll [dice] fX tY`\tSpecifies the target number that must be met (X), with Y focus added to the result"

# Posts a link to this GitHub repository
def github_link(message_content, message_author):
    return "We have a GitHub! Check out the code used to make this bot at `https://github.com/ThomasDearth/Dice-Haver`. We'd love to hear your suggestions!"

# Notifies the client that the program has connected to the server correctly
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

# Activates whenever someone posts a message
@client.event
async def on_message(message):
    # If the bot posted the message, don't respond to it.
    if message.author == client.user:
        return

    if not message.content.startswith("!"):
        return
    else:
        cases = {
            "!roll" : command_modules.roll.roll_message_parse,
            "!help" : help_message,
            "!github" : github_link
        }
        if message.content.split(" ")[0] not in cases:
            await message.channel.send("Error: not a valid command. For help, type `!help`")
        else:
            await message.channel.send(cases.get(message.content.split(" ")[0])(clean(message.content), message.author))

print("2")
client.run(TOKEN)
