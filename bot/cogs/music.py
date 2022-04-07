import asyncio

import discord
from discord.ext import commands

from yt_dlp import YoutubeDL as yt_dlp
from shortcuts import misc

ytdl_opts = {'format': 'bestaudio/audio', "quiet": True}
ffmpeg_opts = {"bopts": "-reconnect 1", "opts": "-vn"}


class Music(commands.Cog, name="Music", description="Music commands"):
    def __init__(self, bot):
        Music.color = discord.Color.random()
        self.logger = bot.logger
        self.bot = bot

        self.music_queue = []
        self.queue_index = 0
        self.ctx = ""

    def search_yt(self, video):
        self.logger.log("info", "search_yt", f"Searching for '{video}'..")
        with yt_dlp(ytdl_opts) as yt_l:
            info = yt_l.extract_info(f"ytsearch:{video}", download=False)["entries"][0]
        self.logger.log("info", "search_yt", f"Found '{info['title']}' ({info['display_id']})")
        result = {
            "hls": info["url"],
            "url": info["original_url"],
            "title": info["title"],
            "artist": info["uploader"],
            "length": info["duration"]
        }
        return result


    # {[{"hls": url}, <vc>, <auth>]}
    async def play_music(self):
        if len(self.music_queue) > self.queue_index:
            song = self.music_queue[self.queue_index][0]
            vc = self.music_queue[self.queue_index][1]
            author = self.music_queue[self.queue_index][2]

            embed = discord.Embed(
                title="Now playing",
                description=f"{song['artist']} - {song['title']} [{author.mention}]",
                color=discord.Color.random()
            )
            await self.ctx.send(embed=embed)
            self.logger.log('info', "play_music", f"Sent '{embed.title}' embed")

            self.queue_index += 1

            self.logger.log('info', "play_music", f"Playing '{song['title']}'")
            vc.play(discord.FFmpegPCMAudio(song["hls"], before_options=ffmpeg_opts["bopts"], options=ffmpeg_opts["opts"]),
                    after=lambda play: asyncio.run_coroutine_threadsafe(self.play_music(), self.bot.loop))

    @commands.command(name="join", brief="Joins vc")
    async def join(self, ctx):
        voice_client = ctx.guild.voice_client
        author_voice = ctx.author.voice

        if author_voice:
            vc = author_voice.channel

            if not voice_client:
                await vc.connect()
                self.ctx = ctx
            else:
                await voice_client.move_to(vc)
        else:
            raise commands.errors.ChannelNotFound("Author not in any voice channel")

        self.logger.log("info", "join", f"Joined {ctx.guild + '/' + vc}")
        await ctx.send(f"Joined `{vc}`!")

    @commands.command(name="play")
    async def play(self, ctx, *args):
        args = " ".join(args)
        voice_client = ctx.guild.voice_client
        vc = ctx.author.voice

        if not vc:
            raise commands.errors.ChannelNotFound("Author not in any voice channel")
        elif not voice_client:
            raise commands.errors.ChannelNotFound("Bot not in any voice channel")
        else:
            async with ctx.typing():
                song = self.search_yt(args)
                self.music_queue.append([song, voice_client, ctx.author])
            self.logger.log("info", "play", f"Added {song['title']} to the queue")
            await ctx.send(f"Added {song['title']} to the queue!")

            if not voice_client.is_playing():
                await self.play_music()

    @commands.command(name="queue", brief="shows the queue")
    async def queue(self, ctx):
        if self.music_queue:
            result = misc.queue_format(self.music_queue, self.queue_index)
            await ctx.send(result)
        else:
            await ctx.send("The queue is empty")


def setup(bot):
    bot.add_cog(Music(bot))
