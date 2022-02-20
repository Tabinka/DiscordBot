import discord
import os
from discord.ext import commands, tasks
from decouple import config
from itertools import cycle

client = commands.Bot(command_prefix="!")
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