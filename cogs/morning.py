import discord
from discord.ext import commands, tasks
import requests
import json
import os
import datetime as dt

WEATHER_API = os.environ['WEATHER_API']
NEWS_API = os.environ['NEWS_API']
WEATHER_URL = "https://api.openweathermap.org/data/2.5/onecall"
QUOTES_URL = "https://quotes.rest/qod"
NEWS_URL = "https://newsapi.org/v2/top-headlines"
SVATKY_URL = "https://svatky.adresa.info/json"


class Morning(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.news_parameters = {
            "apiKey": NEWS_API,
            "country": "us",
            "category": "general"
        }
        self.weather_parameters = {
            "lat": 49.67763,
            "lon": 18.67078,
            "units": "metric",
            "appid": WEATHER_API
        }
        self.channels = self.client.get_channel(870725266123677726)
        self.morning_routine.start()


    def check_time(self):
        time_now = dt.datetime.now().time()
        formatted = time_now.strftime("%H")
        return formatted
    
    # TODO: Recreate that function to be more ellegant
    @tasks.loop(hours=1)
    async def morning_routine(self):
        if(self.check_time() == "07"):
            svatky_response = requests.get(url=SVATKY_URL)
            news_response = requests.get(url=NEWS_URL, params=self.news_parameters)
            weather_response = requests.get(url=WEATHER_URL, params=self.weather_parameters)
            quotes_response = requests.get(url=QUOTES_URL)

            news = news_response.json()["articles"][:5]
            articles = ""
            for n_title in news:
                articles += n_title["title"]
                articles += " ("
                articles += n_title["url"]
                articles += ") \n\n"
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
                f"quote**\n *{random_quote}*\n\n**Fresh news**\n{articles}")
        
        
def setup(client):
    client.add_cog(Morning(client))