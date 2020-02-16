import asyncio

import discord
import youtube_dl

from discord.ext import commands

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

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
    async def play(self, ctx: commands.Context, *, url= 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'):
        ctxChannel = ctx.author.voice.channel
        if not self.check_voice_chat_connection(ctx):
            await ctx.invoke(self.join)

        """
        async with ctx.typing():
            with ([c for c in self.client.voice_clients if c.channel.id == ctxChannel.id][0]) as voice_client:
                source = discord.FFmpegPCMAudio('music.mp3')
                voice_client.play(source, after=lambda e: print('done', e))
                voice_client.start()
        #"""
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.client.loop)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

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