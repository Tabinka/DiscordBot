import discord
import datetime as dt
from discord.channel import DMChannel
from discord.ext import commands, tasks
from decouple import config
import requests
import requests.auth
import json
import html
import time

RAPID_API_KEY = config('RAPID_API_KEY')


class Netflix(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.channel = client.get_channel(797512794081460226)
        self.url = "https://unogs-unogs-v1.p.rapidapi.com/aaapi.cgi"
        self.querystring = {"q": "get:new1:US",
                            "p": "1", "t": "ns", "st": "adv"}
        self.headers = {
            'x-rapidapi-host': "unogs-unogs-v1.p.rapidapi.com",
            'x-rapidapi-key': RAPID_API_KEY
        }
        # self.get_new_content.start()

    @commands.command()
    async def netflix_upcomming(self, ctx):
        await ctx.send("Upcomming netflix 💩")

    @tasks.loop(hours=24)
    async def get_new_content(self):
        response = requests.request(
            "GET", self.url, headers=self.headers, params=self.querystring)
        data_count = int(response.json()["COUNT"])
        if data_count > 0:
            for item in response.json()["ITEMS"]:
                time.sleep(5)
                title = html.unescape(item['title'])
                synopsis = html.unescape(item['synopsis'])
                text = f"**Netflix released new content!** 🙈\n\n**{title}**\n\n*{synopsis}\n\nType:{item['type']}*" \
                    f"\n\n{item['image']}"
                await self.channel.send(text)


def setup(client):
    client.add_cog(Netflix(client))
