import discord, logging
from discord.channel import DMChannel
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, MissingPermissions
import re

# TODO: Error messages


class Basic(commands.Cog, description="Basic commands for fun and magic."):
    def __init__(self, client):
        self.client = client

    # Event logs when a member joins a server
    # TODO: Test if user with Chinese characters is banned after joining the server or not
    @commands.Cog.listener()
    async def on_member_join(self, member):
        for letter in member.name:
            if re.search("[\u4e00-\u9fff]", letter):
                logging.warning(f"A {member} has a chinese character in name. He is banned.")
                member.ban()
            else:
                logging.info(f"A {member} has joined a server.")

    # Event logs when a member is removed from a server
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        logging.info(f"{member} has left a server.")

    @commands.command(brief="Check bot response time.")
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.client.latency * 1000)}ms")

    # TODO: Add more features for posting animated emojis (like hypemode etc..)
    @commands.command(brief="Spawn animated emojis with a party blop!")
    async def party(self, ctx):
        party = "<a:apartyblob:857886687458885672> <a:apartyblob:857886687458885672> <a:apartyblob:857886687458885672> <a:apartyblob:857886687458885672> <a:apartyblob:857886687458885672> <a:apartyblob:857886687458885672> <a:apartyblob:857886687458885672>"
        await ctx.send(party)
        
    @commands.command(brief="Spawn animated emojis with a vibes!")
    async def vibes(self, ctx):
        vibes = "<a:vibes:857896704472776705> <a:vibes:857896704472776705> <a:vibes:857896704472776705> <a:vibes:857896704472776705> <a:vibes:857896704472776705>"
        await ctx.send(vibes)
        
    @commands.command(brief="Spawn animated emojis with upvoteVibes!")
    async def upvote(self, ctx):
        upvote = "<a:upvoteVibes:857896715402870794> <a:upvoteVibes:857896715402870794> <a:upvoteVibes:857896715402870794> <a:upvoteVibes:857896715402870794>"
        await ctx.send(upvote)
        
    @commands.command(brief="Spawn animated emojis with pepeFast!")
    async def pepefast(self, ctx):
        pepefast = "<a:pepeFast:878174253378322452> <a:pepeFast:878174253378322452> <a:pepeFast:878174253378322452> <a:pepeFast:878174253378322452>"
        await ctx.send(pepefast)
        
    @commands.command(brief="Spawn animated emojis with pepeSmoke!")
    async def pepesmoke(self, ctx):
        pepesmoke = "<a:pepeSmoke:878174230221582376> <a:pepeSmoke:878174230221582376> <a:pepeSmoke:878174230221582376> <a:pepeSmoke:878174230221582376>"
        await ctx.send(pepesmoke)
        
    @commands.command(brief="Spawn animated emojis with nootnoot!")
    async def noot(self, ctx):
        noot = "<a:Nootnoot:878183535746359337> <a:Nootnoot:878183535746359337> <a:Nootnoot:878183535746359337> <a:Nootnoot:878183535746359337>"
        await ctx.send(noot)

    @commands.command(brief="Spawn animated emoji with a gabihomesick!")
    async def gabihomesick(self, ctx):
        emoji = "<a:gabihomesick:878180337514057769><a:gabihomesick:878180337514057769><a:gabihomesick:878180337514057769>"
        await ctx.send(emoji)

    @commands.command(brief="Spawn animated emoji with a lil swag!")
    async def swag(self, ctx):
        emoji = "<a:lil_swag:857892198674726922><a:lil_swag:857892198674726922><a:lil_swag:857892198674726922>"
        await ctx.send(emoji)

    @commands.command(brief="Spawn HYPE!! emojis!")
    async def hype(self, ctx):
        emoji = "<a:200:865494877143040031> <a:200:865494877143040031> <a:200:865494877143040031> <a:200:865494877143040031> <a:200:865494877143040031>"
        await ctx.send(emoji)

    @commands.command(brief="Clear messages from channel.")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify amounts of messages to delete.")

    @commands.command(
        brief="Kick someone from server if they are anoying (admin only)."
    )
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        logging.info(f"User {member.mention} was kicked.")
        await ctx.send(f"User {member.mention} was kicked.")

    @commands.command(
        brief="Ban someone from server if they are very naughty (admin only)."
    )
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        logging.info(f"User {member.mention} was banned.")
        await ctx.send(f"User {member.mention} was banned.")

    @commands.command(
        brief="Unban someone from server if they are good again (admin only)."
    )
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for banned_entry in banned_users:
            user = banned_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                logging.info(f"User {member.mention} was unbanned.")
                await ctx.send(f"User {user.mention} was unbanned.")
                return


async def setup(client):
    await client.add_cog(Basic(client))
