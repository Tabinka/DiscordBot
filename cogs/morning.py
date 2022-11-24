import logging
import discord
from discord.ext import commands, tasks
import requests
import os
import datetime as dt

WEATHER_API = os.environ["WEATHER_API"]
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
            "appid": WEATHER_API,
        }
        self.morning_routine.start()

    def check_time(self):
        time_now = dt.datetime.now().time()
        formatted = time_now.strftime("%H")
        return formatted

    # TODO: Recreate that function to be more elegant
    @tasks.loop(hours=1)
    async def morning_routine(self):
        if self.check_time() == "07":
            try:
                channel = client.get_channel(870725266123677726)
                svatky_response = requests.get(url=SVATKY_URL)
                weather_response = requests.get(
                    url=WEATHER_URL, params=self.weather_parameters
                )
                quotes_response = requests.get(url=QUOTES_URL)

                if svatky_response and weather_response and quotes_response:
                    random_quote = quotes_response.json()["contents"]["quotes"][0][
                        "quote"
                    ]
                    data = weather_response.json()
                    svatek_name = ""
                    svatky = svatky_response.json()
                    for svatek in svatky:
                        svatek_name += f"{svatek['name']} "
                    weather_type = data["current"]["weather"][0]["description"]
                    temp = round(data["current"]["temp"])

                    embedM = discord.Embed(
                        title="**☕️ Good Morning! ☀**",
                        color=discord.Color.yellow(),
                        description=f"Today is *{dt.datetime.now().date().strftime('%A - %d.%m.')}* and name day has *{svatek_name}*\n\nWeather for today is going to be *{weather_type} and {temp}°C*\n\n**Your random motivational quote**\n *{random_quote}*",
                    )
                    embedM.set_footer(
                        text="Don't forget to wash your balls and face. Thank you! 🤓"
                    )
                    await channel.send(embed=embedM)

                else:
                    raise ValueError("One of the response is empty.")
            except (AttributeError, KeyError, ValueError):
                logging.error("Morning routine was not successful.")
                await self.morning_routine()


async def setup(client):
    await client.add_cog(Morning(client))
