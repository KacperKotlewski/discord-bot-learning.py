import discord
from discord.ext import commands
import youtube_dl
youtube_dl.utils.bug_reports_message = lambda: ''

class Voice(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(invoke_without_subcommand=True)
    async def join(self, ctx: commands.Context):
        channel = ctx.author.voice.channel
        await channel.connect()

    @commands.command()
    async def leave(self, ctx: commands.Context):
        for con in self.client.voice_clients:
            if con.channel.id == ctx.author.voice.channel.id:
                await con.disconnect(force=False)

    def check_voice_chat_connection(self, ctx: commands.Context):
        return ctx.author.voice.channel.id in [c.channel.id for c in self.client.voice_clients]

    @commands.command()
    async def play(self, ctx: commands.Context, url=""):
        ctxChannel = ctx.author.voice.channel
        if not self.check_voice_chat_connection(ctx):
            await ctx.invoke(self.join)

        async with ctx.typing():
            voice_client = ([c for c in self.client.voice_clients if c.channel.id == ctxChannel.id][0])
            voice_client.play(discord.FFmpegPCMAudio('music.mp3'), after=lambda e: print('done', e))
            voice_client.start()

    @commands.command()
    async def stop(self, ctx: commands.Context):
        if self.check_voice_chat_connection(ctx):
            ctxChannel = ctx.author.voice.channel
            ([c for c in self.client.voice_clients if c.channel.id == ctxChannel.id][0]).stop()
            await ctx.invoke(self.leave)

    @commands.command()
    async def pause(self, ctx:commands.Context):
        if self.check_voice_chat_connection(ctx):
            ctxChannel = ctx.author.voice.channel
            ([c for c in self.client.voice_clients if c.channel.id == ctxChannel.id][0]).pause()

    @commands.command()
    async def resume(self, ctx:commands.Context):
        if self.check_voice_chat_connection(ctx):
            ctxChannel = ctx.author.voice.channel
            ([c for c in self.client.voice_clients if c.channel.id == ctxChannel.id][0]).resume()





    @commands.command()
    async def playing(self, ctx: commands.Context):
        channel_id = ctx.author.voice.channel.id
        for con in self.client.voice_clients:
            if con.channel.id == channel_id:
                vc = con
                await ctx.send(vc.is_playing())


def setup(client):
    client.add_cog(Voice(client))