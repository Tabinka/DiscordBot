import discord
import random
from discord.ext import commands


class Games(commands.Cog, description="Few commands for fun and games"):
      def __init__(self, client):
            self.client = client

      @commands.command(aliases=["8ball", "8ballgame"])
      async def _8ball(self, ctx, *, question):
            responses = [
                  "It is certain.",
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
                  "Very doubtful.",
            ]
            await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")

      
      @commands.command()
      async def rps(self, ctx, *, option):
            val_options = ["rock", "paper", "scissors"]
            title = "Rock Paper Scissors game"
            if option in val_options:
                  bot_value = random.choice(val_options)
                  description = f"You have challenged me in rps game! \n My pick is: {bot_value} \n Your pick is: {option} \n Result: "
                  if option == bot_value:
                        description += "Draw!"
                  elif (option == "rock" and bot_value == "scissors") or (option == "paper" and bot_value == "rock") or (option == "scissors" and bot_value == "paper"):
                        description += "You won!"
                  else:
                        description += "I won!"
                  embedMess = discord.Embed(
                    title=title, color=discord.Color.red(), description=description
                  )
            else:
                  description = "Wrong input. Please try again."
                  embedMess = discord.Embed(
                    title=title, color=discord.Color.red(), description=description
                  )
            await ctx.send(embed=embedMess)


async def setup(client):
    await client.add_cog(Games(client))
