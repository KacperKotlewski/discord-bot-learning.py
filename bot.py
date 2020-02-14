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
    #game = discord.Game("with the API")
    #client.change_presence(status=discord.Status.idle, activity=game)

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

@client.command(aliases=["reset", "restart", "reboot"])
async  def reset(ctx):
    await ctx.send("wait i need few sec to think about this")
    await client.close()
    import os
    os.system("cls")
    os.system("echo bot restarting")
    os.system("python bot.py "+str(token))


client.run(token)