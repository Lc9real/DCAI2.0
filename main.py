import message_handler
from datetime import datetime
import re
import discord
from discord import app_commands
import os

def run_discord_bot():
    TOKEN = open("Info.txt", "r").readlines()[0][6:]
    intents = discord.Intents(messages=True, guilds=True, message_content=True, members=True)

    client = discord.Client(intents=intents)
    tree = app_commands.CommandTree(client)
    @client.event
    async def on_ready():
        await tree.sync()
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        if message.guild:
            await message_handler.send_message(message, False, client)
        else:
            await message_handler.send_message(message, True, client)
    client.run(TOKEN)

run_discord_bot()


