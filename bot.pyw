# bot.py
import os
import discord
from dotenv import load_dotenv
import dice_handler

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

# Removes duplicate spaces from a message and converts it to lowercase
def clean(message):
    message = message.lower()
    message = " ".join(message.split())
    return message

def help_message(message_content, message_author):
    return "@" + str(message_author)[:len(str(message_author))-5] + " Hi! I'm a dice-rolling bot for your discord servers!\nBasic commands:\n`!help`\t displays this page\n\nSimple dice rolls:\n`!roll N`\t rolls *N* six-sided dice\n`!roll dN`\t rolls one die with *N* sides\n`!roll XdY`\t rolls *X* dice with *Y* sides each\n\nSoulbound-specific tools:\n`!roll [dice] tX`\tSpecifies the target number (x) a die must meet\n`!roll [dice] fX tY`\tSpecifies the target number that must be met (X), with Y focus added to the result"

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if not message.content.startswith("!"):
        return
    else:
        cases = {
            "!roll" : dice_handler.roll_message_parse,
            "!help" : help_message
        }
        if message.content.split(" ")[0] not in cases:
            await message.channel.send("Error: not a valid command. For help, type `!help`")
        else:
            await message.channel.send(cases.get(message.content.split(" ")[0])(clean(message.content), message.author))

client.run(TOKEN)
