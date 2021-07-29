import discord
import os
import requests
import json
import random
import datetime
from dotenv import load_dotenv

client = discord.Client()

greetings = ["hello", "hi", "greetings", "sup", "howdy", "peekaboo"]
botGreetings = ["*drops from behind you* Hello there!",
                "Howdy partner *tips hat*"]


def getQuote():
    response = requests.get("https://zenquotes.io/api/random")
    jsonData = json.loads(response.text)
    quoteEmbed = discord.Embed(title="Inspirational Quote", color=0xdb0000)
    quoteEmbed.set_author(name="ADedicatedCoder", url="https://github.com/MahinKukreja",
                          icon_url="https://avatars.githubusercontent.com/u/40774998?s=400&v=4")
    quoteEmbed.add_field(name="Quote", value=jsonData[0]["q"], inline=True)
    quoteEmbed.add_field(name="Author", value=jsonData[0]["a"], inline=False)
    quoteEmbed.set_footer(text="Provided by zenquotes.io")
    return quoteEmbed


def getCovidStats(country):
    fetchUrl = f"https://disease.sh/v3/covid-19/countries/{country}?strict=true"
    response = requests.get(fetchUrl)
    jsonData = json.loads(response.text)
    countryName = jsonData["country"]
    updatedTime = (datetime.datetime.fromtimestamp(
        jsonData["updated"]/1000)).strftime("%m/%d/%Y - %H:%M:%S GMT")
    try:
        covidEmbed = discord.Embed(
            title=f"COVID-19 Statistics for {countryName}", url=fetchUrl, color=0xdb0000)
        covidEmbed.set_author(name="ADedicatedCoder", url="https://github.com/MahinKukreja",
                              icon_url="https://avatars.githubusercontent.com/u/40774998?s=400&v=4")
        covidEmbed.add_field(
            name="Total Cases", value="{:,}".format(jsonData["cases"]), inline=False)
        covidEmbed.add_field(
            name="Total Deaths", value="{:,}".format(jsonData["deaths"]), inline=False)
        covidEmbed.add_field(
            name="Total Recovered", value="{:,}".format(jsonData["recovered"]), inline=False)
        covidEmbed.add_field(
            name="Data from Time", value=updatedTime, inline=False)
        covidEmbed.set_footer(
            text="Information provided by disease.sh - Open Disease Data API")
    except KeyError:
        return "Code invalid/country not supported. Check ISO codes here: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3"

    return covidEmbed


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="with Python3"))
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message):
    msg = message.content
    chnl = message.channel

    if message.author == client.user:
        return

    if msg.startswith("!ping"):
        await chnl.send(f"Pong! ({round(client.latency * 1000)}ms)")

    if msg.startswith("!inspire"):
        await chnl.send(embed=getQuote())

    if msg.startswith("!covid"):
        country = (msg.split("!covid ", 1)[1]).upper()
        await chnl.send(embed=getCovidStats(country))

    if msg.startswith("!help"):
        await chnl.send("Type `!covid COUNTRYISO3CODE` where `COUNTRYISO3CODE` is the code of your country. Find all the codes at https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3")

    if any(word in msg for word in greetings):
        await chnl.send(random.choice(botGreetings))


load_dotenv()
client.run(os.getenv("TOKEN"))
