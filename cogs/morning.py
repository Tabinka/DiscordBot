import discord
from discord.ext import commands, tasks
import requests
import json
import os
import datetime as dt

WEATHER_API = os.environ['WEATHER_API']
WEATHER_URL = "https://api.openweathermap.org/data/2.5/onecall"
QUOTES_URL = "https://quotes.rest/qod"
SVATKY_URL = "https://svatky.adresa.info/json"


class Morning(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.weather_parameters = {
            "lat": 49.67763,
            "lon": 18.67078,
            "units": "metric",
            "appid": WEATHER_API
        }
        self.channels = self.client.get_channel(797512794081460226)
        self.morning_routine.start()


    def check_time(self):
        time_now = dt.datetime.now().time()
        formatted = time_now.strftime("%H")
        return formatted
    
    # TODO: Recreate that function to be more ellegant
    @tasks.loop(hours=1)
    async def morning_routine(self):
        if(self.check_time() == "07"):
            try:
                svatky_response = requests.get(url=SVATKY_URL)
                weather_response = requests.get(url=WEATHER_URL, params=self.weather_parameters)
                quotes_response = requests.get(url=QUOTES_URL)

                random_quote = quotes_response.json()["contents"]["quotes"][0]["quote"]
                data = weather_response.json()
                svatek_name = ""
                svatky = svatky_response.json()
                for svatek in svatky:
                    svatek_name += f"{svatek['name']} "
                weather_type = data["current"]["weather"][0]["description"]
                temp = round(data["current"]["temp"])
                
                await self.channels.send(
                    f"**Good Morning!** ☀️ \n\nToday is {dt.datetime.now().date().strftime('%A - %d.%m.')} and name day has "
                    f"{svatek_name}\n\nWeather for today is going to be {weather_type} and {temp}°C\n\n**Your random motivational "
                    f"quote**\n *{random_quote}")
            except (AttributeError, KeyError):
                await self.morning_routine()
        
        
def setup(client):
    client.add_cog(Morning(client))