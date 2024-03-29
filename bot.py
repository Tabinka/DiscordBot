import discord, logging
import asyncio
import os
import logging
import logging.handlers
from discord.ext import commands, tasks
from pretty_help import DefaultMenu, PrettyHelp
from itertools import cycle
from dotenv import load_dotenv
import giphy_client
from giphy_client.rest import ApiException

load_dotenv()

## Settings for custom help menu
menu = DefaultMenu(page_left="🤛", page_right="🤜", remove="🌊", active_time=15, delete_after_timeout=45)

## Important stuff for Discord
intents = discord.Intents.all()

## Giphy API call
api_instance = giphy_client.DefaultApi()
api_key = os.environ["GIPHY_API"]
tag = "hello"

## Initialize logger and start logging to discord.log
logger = logging.getLogger("discord")
logger.setLevel(logging.WARNING)
logging.getLogger("discord.http").setLevel(logging.WARNING)

handler = logging.handlers.RotatingFileHandler(
    filename="discord.log",
    encoding="utf-8",
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
)
handler.setFormatter(formatter)
logger.addHandler(handler)

client = commands.Bot(
    command_prefix="!", help_command=PrettyHelp(menu=menu), intents=intents, case_insensitive = True
)
status = cycle(["I am clowning here.", "Making plans for world dominantion."])

# Event prints in console when bot is ready to use
@client.event
async def on_ready():
    change_status.start()
    guilds = [guild async for guild in client.fetch_guilds(limit=10)] ## Only temporary, TODO: Need to change for better solution
    
    if "421597335248699392" in guilds:
        try:
            api_response = api_instance.gifs_random_get(api_key=api_key, tag=tag)
            ## TODO: Bug with embeds, need to check it
            # embed=discord.Embed(title="Hello there")
            channel = client.get_channel(870725266123677726)
            await channel.send(
                content=f"**Bot has spawned**🤖\n\nHello there tiny humans. I am back and even stronger! 😈 \n{api_response.data.url}"
            )
        except ApiException as e:
            logging.error("Exception when calling DefaultApi->gifs_random_get: %s\n" % e)
    print("Bot is online! 🤖")


@tasks.loop(seconds=500)
async def change_status():
    await client.change_presence(
        status=discord.Status.idle, activity=discord.Game(next(status))
    )


@client.command()
async def load(ctx, extension):
    await client.load_extension(f"cogs.{extension}")


@client.command()
async def unload(ctx, extension):
    await client.unload_extension(f"cogs.{extension}")


@client.command()
async def reload(ctx, extension):
    await client.unload_extension(f"cogs.{extension}")
    await client.load_extension(f"cogs.{extension}")


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with client:
        await load_extensions()
        await client.start(os.environ["DISCORD_KEY"])


asyncio.run(main())
