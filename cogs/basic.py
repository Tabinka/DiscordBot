import discord
from discord.channel import DMChannel
from discord.ext import commands, tasks
from itertools import cycle


class Basic(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.status = cycle(
            ["I am clowning here.", "Making plans for world dominantion."])
        # self.change_status.start()

    # Event prints in console when bot is ready to use
    # TODO: Add sending funny little message into dedicated channel about bot being ready
    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is online! 🤖")

    # Event prints in console when a member joins a server
    # TODO: Add function to inform whole server about user joining a server in dedicated channel
    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f"A {member} has joined a server.")

    # Event prints in console when a member is removed from a server
    # TODO: Add function to inform whole server about it in a dedicated channel
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f"{member} has left a server.")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.client.latency * 1000)}ms")

    @tasks.loop(seconds=500)
    async def change_status(self):
        await self.client.change_presence(status=discord.Status.idle, activity=discord.Game(next(self.status)))


def setup(client):
    client.add_cog(Basic(client))
