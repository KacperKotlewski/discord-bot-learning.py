import discord
from discord.ext import commands

class Utilities(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def clean(self, ctx, amount=2):
        await ctx.channel.purge(limit=amount)
        print(type(ctx))

    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await ctx.send(f"sorry dude @{member} you been randomly picked to been kicked")
        await member.kick(reason=reason)
        await  ctx.send(f"{member.mention} has drop out")

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)

    @commands.command()
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminatior = member.split('#')

        for ban_entity in banned_users:
            user = ban_entity.user

            if (user.name, user.discriminator) == (member_name, member_discriminatior):
                await ctx.guild.unban(user)
                await ctx.send(f"{user.mention} has been unbaned")

    @commands.command(aliases=["8ball"])
    async def _8ball(self, ctx, *, question):
        import random
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

def setup(client):
    client.add_cog(Utilities(client))