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

client.run(token)