import discord
from discord.ext import commands
import requests
import requests.auth
import html
import time
import os

RAPID_API_KEY = os.environ["RAPID_API_KEY"]


class Netflix(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.channel = client.get_channel(797512794081460226)
        self.url = "https://unogs-unogs-v1.p.rapidapi.com/aaapi.cgi"
        self.querystring = {"q": "get:new1:CZ", "p": "1", "t": "ns", "st": "adv"}
        self.headers = {
            "x-rapidapi-host": "unogs-unogs-v1.p.rapidapi.com",
            "x-rapidapi-key": RAPID_API_KEY,
        }

    # TODO: Add command for random movie / TV series pick

    # TODO: Refactor this code for command
    @commands.command()
    async def get_new_content(self, ctx):
        response = requests.request(
            "GET", self.url, headers=self.headers, params=self.querystring
        )
        data_count = int(response.json()["COUNT"])
        if data_count > 0:
            for item in response.json()["ITEMS"]:
                time.sleep(5)
                title = html.unescape(item["title"])
                synopsis = html.unescape(item["synopsis"])
                embedMess = discord.Embed(
                    title=title, color=discord.Color.red(), description=synopsis
                )
                embedMess.set_thumbnail(url=item["image"])
                await ctx.send(embed=embedMess)


async def setup(client):
    await client.add_cog(Netflix(client))
