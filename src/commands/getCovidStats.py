# Import necessary libraries
from logging import log
import discord
import requests
import json
import datetime
from dotenv import load_dotenv

with open("./data/countryToISO.json") as database:
    countries = json.load(database)


def getCovidStats(country):
    fetchUrl = "http://localhost:8080/bot"
    inputData = {"country": country.upper()}
    postReq = requests.post(fetchUrl, data=inputData)

    if postReq.status_code == 200:
        jsonData = json.loads(postReq.text)["stats"]
        updatedTime = (datetime.datetime.fromtimestamp(
            jsonData["updated"]/1000)).strftime("%m/%d/%Y - %H:%M:%S GMT")
        covidEmbed = discord.Embed(
            title="COVID-19 Statistics for " + jsonData["country"], color=0xdb0000)
        covidEmbed.set_thumbnail(url=jsonData["flag"])
        covidEmbed.set_author(name="ADedicatedCoder", url="https://github.com/MahinKukreja",
                              icon_url="https://avatars.githubusercontent.com/u/40774998?s=400&v=4")
        covidEmbed.add_field(
            name="Total Cases", value="{:,}".format(jsonData["cases"]), inline=False)
        covidEmbed.add_field(
            name="Total Deaths", value="{:,}".format(jsonData["deaths"]), inline=False)
        covidEmbed.add_field(
            name="Total Recovered", value="{:,}".format(jsonData["cured"]), inline=False)
        covidEmbed.add_field(
            name="Data from Time", value=updatedTime, inline=False)
        covidEmbed.set_footer(
            text="Information provided by disease.sh - Open Disease Data API")

    else:
        covidEmbed = discord.Embed(
            title="Failure", description="Please double check spelling", color=0xbb0000)
        covidEmbed.set_thumbnail(
            url="https://cdn0.iconfinder.com/data/icons/shift-free/32/Error-512.png")
        covidEmbed.set_author(name="ADedicatedCoder", url="https://github.com/MahinKukreja",
                              icon_url="https://avatars.githubusercontent.com/u/40774998?s=400&v=4")
        covidEmbed.add_field(
            name="Error", value="Country not found", inline=False)
        covidEmbed.set_footer(
            text="Information provided by disease.sh - Open Disease Data API")

    return covidEmbed
