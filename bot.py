import sys
import discord
from discord.ext import commands

if len(sys.argv)>1:
    token = sys.argv[1]
else:
    import config
    token = config.DISCORD_BOT_TOKEN

client = commands.Bot(command_prefix="//")

@client.event
async def on_ready():
    print('hello i\'m alive')

@client.event
async def on_member_join(member):
    print(f"{member} has join to server")

@client.event
async def on_member_remove(member):
    print(f"{member} has left the server")

@client.command()
async def ping(ctx): #ctx context
    await ctx.send(f"Pong! {round(client.latency*1000)}ms")

import random
@client.command(aliases=["8ball"])
async  def _8ball(ctx, *, question):
    response = ["It is certain.",
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
    await ctx.send(f"Question: {question}\nAnswer: {random.choice(response)}")

client.run(token)