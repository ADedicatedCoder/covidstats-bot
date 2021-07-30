# Import necessary libraries
from logging import log
import discord
import os
import json
from dotenv import load_dotenv
from src.commands.getCovidStats import getCovidStats
from src.commands.ping import returnPing
from src.commands.keepEmoji import keepEmojis
import time

client = discord.Client()

with open("./data/countryToISO.json") as database:
    countries = json.load(database)


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.dnd, activity=discord.Game(name="with Python3"))
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message):
    print(message.channel.id)
    msg = message.content
    chnl = message.channel

    if message.author == client.user:
        return

    if msg.startswith("!ping"):
        await chnl.send(returnPing(client))

    if msg.startswith("!covid"):
        country = (msg.split("!covid ", 1)[1]).upper()
        await chnl.send(embed=getCovidStats(country))

    if message.channel.id == 856287087980576799:
        await chnl.purge(limit=keepEmojis(msg))
        await chnl.send("NOT ALLOWED")
        time.sleep(5)
        await chnl.purge(limit=1)


load_dotenv()
client.run(os.getenv("TOKEN"))
