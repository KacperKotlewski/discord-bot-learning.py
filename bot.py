import sys
import discord
import os
from discord.ext import commands
import config

if len(sys.argv)>1:
    token = sys.argv[1]
else:
    token = config.DISCORD_BOT_TOKEN

client = commands.Bot(command_prefix=config.DISCORD_BOT_PREFIX)

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