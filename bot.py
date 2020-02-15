import sys
import discord
import os
from discord.ext import commands, tasks
from itertools import cycle
import config

if len(sys.argv)>1:
    token = sys.argv[1]
else:
    token = config.DISCORD_BOT_TOKEN

client = commands.Bot(command_prefix=config.DISCORD_BOT_PREFIX)

@client.event
async def on_ready():
    pinging.start()

status = cycle(["Feedbacking questions", "Doing stuff", "Getting rage"])
@tasks.loop(seconds=10)
async def pinging():
    import random
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game(status)
    )

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please pass all required arguments")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Command don't exist")

@client.command()
async def load(ctx, extension):
    try:
        client.load_extension(f"cogs.{extension}")
        await ctx.send(f"Loaded {extension}")
    except discord.ext.commands.errors.ExtensionNotFound:
        await ctx.send(f"Extension {extension}.py don't exist")

@client.command()
async def unload(ctx, extension):
    try:
        client.unload_extension(f"cogs.{extension}")
        await ctx.send(f"Unloaded {extension}")
    except discord.ext.commands.errors.ExtensionNotLoaded:
        await ctx.send(f"Extension {extension}.py not loaded")

@load.error
@unload.error
async def load_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You need to specify extension")

@client.command()
async def show(ctx, what = ""):
    if(what == "help" or what == "?" or what == ""):
        await ctx.send(f"""```About show command:
    \nsyntax:
    \t{config.DISCORD_BOT_PREFIX}show <value>
    \nvalues:
    \thelp -> describe a command
    \textension -> to show extensions
    \nexample:
    \t{config.DISCORD_BOT_PREFIX}show help
```
""")
    elif(what == "extensions"):
        extensions = ""
        for file in os.listdir("./cogs"):
            if file.endswith(".py"):
                extensions += str(f"{file[:-3]}\n")
        await ctx.send(f"```\nextensions:\n{extensions}```")
    else:
        await ctx.send(f"We don't understand each other :/ try use: ***{config.DISCORD_BOT_PREFIX}show help***")


for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        client.load_extension(f"cogs.{file[:-3]}")

@client.command(aliases=["reset","restart", "reboot"])
async  def _reset(ctx):
    await ctx.send("wait i need few sec to think about this")
    await client.close()
    import os
    os.system("cls")
    os.system("echo bot restarting")
    os.system("python bot.py "+str(token))


client.run(token)