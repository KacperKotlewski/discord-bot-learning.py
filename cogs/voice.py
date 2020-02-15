import discord
from discord.ext import commands

class Voice(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        await channel.connect()

    @commands.command()
    async def leave(self, ctx: commands.context.Context):
        for con in self.client.voice_clients:
            if con.channel.id == ctx.author.voice.channel.id:
                await con.disconnect(force=False)

def setup(client):
    client.add_cog(Voice(client))