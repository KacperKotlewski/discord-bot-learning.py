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
        await ctx.send(f"""
```\nsyntax:
    \t{config.DISCORD_BOT_PREFIX}show <value>
    \nvalues:
    \thelp -> describe a command
    \textension -> to show extensions
    \nexample:
    \t{config.DISCORD_BOT_PREFIX}show help
```
""")
    if(what == "extensions"):
        extensions = ""
        for file in os.listdir("./cogs"):
            if file.endswith(".py"):
                extensions += str(f"{file[:-3]}\n")
        await ctx.send(f"```\nextensions:\n{extensions}```")


for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        client.load_extension(f"cogs.{file[:-3]}")


@client.event
async def on_member_join(member):
    print(f"{member} has join to server")

@client.event
async def on_member_remove(member):
    print(f"{member} has left the server")

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

@client.command()
async def clean(ctx, amount=2):
    await ctx.channel.purge(limit=amount)

@client.command()
async def kick(ctx, member:discord.Member, *, reason=None):
    await ctx.send(f"sorry dude @{member} you been randomly picked to been kicked")
    await member.kick(reason=reason)
    await  ctx.send(f"{member.mention} has drop out")

@client.command()
async  def ban(ctx, member:discord.Member, *, reason=None):
    await member.ban(reason=reason)

@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminatior = member.split('#')

    for ban_entity in banned_users:
        user = ban_entity.user

        if(user.name, user.discriminator) == (member_name, member_discriminatior):
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention} has been unbaned")

@client.command(aliases=["reset","restart", "reboot"])
async  def _reset(ctx):
    await ctx.send("wait i need few sec to think about this")
    await client.close()
    import os
    os.system("cls")
    os.system("echo bot restarting")
    os.system("python bot.py "+str(token))


client.run(token)