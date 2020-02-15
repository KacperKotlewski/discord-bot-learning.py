import discord
from discord.ext import commands, tasks

status = ["Feedbacking questions", "Doing stuff", "Getting rage"]

class Task(commands.Cog):
    def __init__(self, client:discord.Client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("work")
        self.pinging.start()

    @tasks.loop(seconds=10)
    async def pinging(self, ctx):
        import random
        await self.client.change_presence(
            status=discord.Status.online,
            activity=discord.Game(random.choice(status))
        )
        await ctx.send("xd")

def setup(client):
    client.add_cog(Task(client))