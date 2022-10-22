import discord
import os
import logging
import logging.handlers
from discord.ext import commands, tasks
from pretty_help import DefaultMenu, PrettyHelp
from itertools import cycle
from dotenv import load_dotenv

load_dotenv()
        
menu = DefaultMenu(page_left="\U0001F44D", page_right="👎", remove="🌊", active_time=5)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename='discord.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)

client = commands.Bot(command_prefix="!", help_command=PrettyHelp(menu=menu))
status = cycle(["I am clowning here.", "Making plans for world dominantion."])

# Event prints in console when bot is ready to use
# TODO: Add sending funny little message into dedicated channel about bot being ready
@client.event
async def on_ready():
    change_status.start()
    print("Bot is online! 🤖")
    
@tasks.loop(seconds=500)
async def change_status():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game(next(status)))

@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")
    
@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    
@client.command()
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")
    
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        
client.run(os.environ['DISCORD_KEY'])