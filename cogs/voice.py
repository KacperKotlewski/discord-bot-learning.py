import discord
from discord.ext import commands
import youtube_dl
youtube_dl.utils.bug_reports_message = lambda: ''

class Voice(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.players = []

    @commands.command(invoke_without_subcommand=True)
    async def join(self, ctx: commands.Context):
        channel = ctx.author.voice.channel
        await channel.connect()

    @commands.command()
    async def leave(self, ctx: commands.Context):
        for con in self.client.voice_clients:
            if con.channel.id == ctx.author.voice.channel.id:
                await con.disconnect(force=False)

    @commands.command()
    async def play(self, ctx: commands.Context, url=""):

        if not ctx.author.voice.channel.id in [c.channel.id for c in self.client.voice_clients]:
            await ctx.invoke(self.join)



    @commands.command()
    async def playing(self, ctx: commands.Context):
        channel_id = ctx.author.voice.channel.id
        for con in self.client.voice_clients:
            if con.channel.id == channel_id:
                vc = con
                await ctx.send(vc.is_playing())


def setup(client):
    client.add_cog(Voice(client))