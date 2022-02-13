import discord
from discord.channel import DMChannel
from discord.ext import commands, tasks
import random
from itertools import cycle
import datetime as dt
from discord.guild import Guild
import requests
import requests.auth
import json
from decouple import config
import tekore as tk
from tabulate import tabulate
import time
import html

CLIENT_AUTH = requests.auth.HTTPBasicAuth(config('CLIENT_ID'), config('APP_SECRET'))
POST_DATA = {"grant_type": "password", "username": "tabinka", "password": config('REDDIT_PASS')}
REDDIT_HEADERS = {"User-Agent": "Opera/9.64 (Windows NT 5.2; sl-SI) Presto/2.12.312 Version/11.00 by Tabinka"}
WEATHER_API = config('WEATHER_API')
NEWS_API = config('NEWS_API')
WEATHER_URL = "https://api.openweathermap.org/data/2.5/onecall"
RAPID_API_KEY = config('RAPID_API_KEY')
QUOTES_URL = "https://quotes.rest/qod"
NEWS_URL = "https://newsapi.org/v2/top-headlines"
SVATKY_URL = "https://svatky.adresa.info/json"
#SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI = tk.config_from_environment()
#conf = tk.config_from_environment(return_refresh=True)
#SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, SPOTIFY_USER_REFRESH = conf
#token = tk.refresh_user_token(*conf[:2], conf[3])
#spotify = tk.Spotify(token)
PAR = {
    "lat": 49.67763,
    "lon": 18.67078,
    "units": "metric",
    "appid": WEATHER_API
}


def check_time():
    time_now = dt.datetime.now().time()
    formatted = time_now.strftime("%H:%M:%S")
    return formatted


def getting_free_deals():
    reddit_response = requests.post("https://www.reddit.com/api/v1/access_token", auth=CLIENT_AUTH, data=POST_DATA,
                                    headers=REDDIT_HEADERS)
    reddit_access_token = reddit_response.json()["access_token"]

    r_headers = {"Authorization": f"bearer {reddit_access_token}",
                 "User-Agent": "Opera/9.64 (Windows NT 5.2; sl-SI) Presto/2.12.312 Version/11.00 by Tabinka"}
    r_response = requests.get("https://oauth.reddit.com/r/GameDealsFree/new", headers=r_headers, params={"limit": 5})
    previous_day = dt.datetime.today() - dt.timedelta(days=1)
    deal = ""
    for x in r_response.json()["data"]["children"]:
        if previous_day.strftime("%d.%m") <= dt.datetime.utcfromtimestamp(x["data"]["created"]).strftime("%d.%m"):
            deal += x["data"]["title"] + " ( " + x["data"]["url_overridden_by_dest"] + " )" + "\n\n"
    return deal


async def morning_routine():
    news_params = {
        "apiKey": NEWS_API,
        "country": "us",
        "category": "technology"
    }
    s_response = requests.get(url=SVATKY_URL)
    n_response = requests.get(url=NEWS_URL, params=news_params)
    response = requests.get(url=WEATHER_URL, params=PAR)
    q_response = requests.get(url=QUOTES_URL)
    news = n_response.json()["articles"][:5]
    articles = ""
    for n_title in news:
        articles += n_title["title"]
        articles += " ("
        articles += n_title["url"]
        articles += ") \n\n"
    quote = q_response.json()
    random_quote = quote["contents"]["quotes"][0]["quote"]
    data = response.json()
    svatek_name = ""
    svatky = s_response.json()
    for svatek in svatky:
        svatek_name += f"{svatek['name']} "
    weather_type = data["current"]["weather"][0]["description"]
    temp = round(data["current"]["temp"])
    channels = client.get_channel(870725266123677726)
    await channels.send(
        f"**Good Morning!** ☀️ \n\nToday is {dt.datetime.now().date().strftime('%A - %d.%m.')} and name day has "
        f"{svatek_name}\n\nWeather for today is going to be {weather_type} and {temp}°C\n\n**Your random motivational "
        f"quote**\n *{random_quote}*\n\n**Fresh news**\n{articles}")


client = commands.Bot(command_prefix="!")
status = cycle(["I am clowning here.", "Making plans for world dominantion."])


@client.event
async def on_ready():
    change_status.start()
    netflix.start()
    deals.start()
    morning.start()
    print("Bot is ready")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command used.")


@client.event
async def on_member_join(member):
    print(f"A {member} has joined a server.")


@client.event
async def on_member_remove(member):
    print(f"{member} has left a server.")


@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms")


@client.command()
async def weather(ctx):
    weather_response = requests.get(WEATHER_URL, params=PAR)
    weather_json = weather_response.json()
    daily_weather = weather_json["daily"]
    date_data = []
    image_data = []
    temp_data = []
    all_data = []
    for x in daily_weather:
        date = f"\t{dt.datetime.utcfromtimestamp(x['dt']).strftime('%d.%m.')}\t"
        temp = f'\t{str(round(x["temp"]["day"], 1))}°C\t'
        image_data.append((x["weather"][0]["main"]).lower())
        date_data.append(date)
        temp_data.append(temp)
    all_data.append(date_data)
    all_data.append(image_data)
    all_data.append(temp_data)
    t = tabulate(all_data, tablefmt="fancy_grid", stralign="center", numalign="center")
    text = f"""
🌤 **Weather Forecast for today and next 7 days** 🌤
```{t}```"""
    await ctx.send(text)


@client.command(aliases=["8ball", "8ballgame"])
async def _8ball(ctx, *, question):
    responses = ["It is certain.",
                 "It is decidedly so.",
                 "Without a doubt.",
                 "Yes - definitely.",
                 "You may rely on it.",
                 "As I see it, yes.",
                 "Most likely.",
                 "Outlook good.",
                 "Yes.",
                 "Signs point to yes.",
                 "Reply hazy, try again.",
                 "Ask again later.",
                 "Better not tell you now.",
                 "Cannot predict now.",
                 "Concentrate and ask again.",
                 "Don't count on it.",
                 "My reply is no.",
                 "My sources say no.",
                 "Outlook not so good.",
                 "Very doubtful."]
    await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")


@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify amounts of messages to delete.")


@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"User {member.mention} was kicked.")


@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"User {member.mention} was banned.")


@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for banned_entry in banned_users:
        user = banned_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"User {user.mention} was unbanned.")
            return


@client.command(aliases=["free"])
async def free_games(ctx):
    await ctx.send(f"🔥 **Attention please!** 🔥\n\nThere are new free games on my radar!\n\n{getting_free_deals()}")


@tasks.loop(seconds=500)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


@tasks.loop(seconds=1)
async def deals():
    if check_time() == "12:00:01" and getting_free_deals() != "":
        channel = client.get_channel(917509192020008980)
        await channel.send(
            f"🔥 **Attention please!** 🔥\n\nThere are new free games on my radar!\n\n{getting_free_deals()}")


@tasks.loop(seconds=1)
async def morning():
    if check_time() == "06:00:01":
        await morning_routine()
    # elif check_time() == "04:00:01":
    #     for device in spotify.playback_devices():
    #         if device.name == "Pixel 4a (5G)" and device.is_active is False:
    #             spotify.playback_start_context(context_uri="spotify:playlist:6ir1gLDpK0x7JdRozGK8iC",
    #                                            device_id=device.id)
    #             spotify.playback_shuffle(True, device_id=device.id)
    #         else:
    #             print("Spotify did not play in ")
    #             break


@tasks.loop(seconds=1)
async def netflix():
    if check_time() == "23:00:01":
        channel = client.get_channel(931937806144643072)
        url = "https://unogs-unogs-v1.p.rapidapi.com/aaapi.cgi"
        querystring = {"q": "get:new1:US", "p": "1", "t": "ns", "st": "adv"}
        headers = {
            'x-rapidapi-host': "unogs-unogs-v1.p.rapidapi.com",
            'x-rapidapi-key': RAPID_API_KEY
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        data_count = int(response.json()["COUNT"])
        if data_count > 0:
            for item in response.json()["ITEMS"]:
                time.sleep(5)
                title = html.unescape(item['title'])
                synopsis = html.unescape(item['synopsis'])
                text = f"**Netflix released new content!** 🙈\n\n**{title}**\n\n*{synopsis}\n\nType:{item['type']}*" \
                       f"\n\n{item['image']}"
                await channel.send(text)


client.run(config('DISCORD_KEY'))
