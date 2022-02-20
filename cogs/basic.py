import discord
from discord.channel import DMChannel
from discord.ext import commands, tasks

class Basic(commands.Cog):

    def __init__(self, client):
        self.client = client

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
        
        
    # TODO: Add more features for posting animated emojis (like hypemode etc..)
    @commands.command()
    async def party(self, ctx):
        party = "<a:apartyblob:857886687458885672> <a:apartyblob:857886687458885672> <a:apartyblob:857886687458885672> <a:apartyblob:857886687458885672> <a:apartyblob:857886687458885672> <a:apartyblob:857886687458885672> <a:apartyblob:857886687458885672>"
        await ctx.send(party)
        
    @commands.command()
    async def gabihomesick(self, ctx):
        emoji = "<a:gabihomesick:878180337514057769>"
        await ctx.send(emoji)
        
    @commands.command()
    async def swag(self, ctx):
        emoji = "<a:lil_swag:857892198674726922>"
        await ctx.send(emoji)
        
    @commands.command()
    async def hype(self, ctx):
        emoji = "<a:200:865494877143040031> <a:200:865494877143040031> <a:200:865494877143040031> <a:200:865494877143040031> <a:200:865494877143040031>"
        await ctx.send(emoji)


def setup(client):
    client.add_cog(Basic(client))
