import discord
from discord.ext import commands

class Example(commands.Cog):
    def __init__(self, client:discord.Client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('hello i\'m alive')
        await self.client.change_presence(status=discord.Status.idle, activity=discord.Game("Feedbacking questions"))

    @commands.command()
    async def ping(self, ctx):  # ctx context
        await ctx.send(f"Pong! {round(self.client.latency * 1000)}ms")

    @commands.Cog.listener()
    async def on_member_join(member):
        print(f"{member} has join to server")

    @commands.Cog.listener()
    async def on_member_remove(member):
        print(f"{member} has left the server")

def setup(client):
    client.add_cog(Example(client))