"""
kwanCore, a discord.py bot foundation.
Copyright (C) 2022  dopebnan

You should have received a copy of the GNU General Public License
along with kwanCore. If not, see <https://www.gnu.org/licenses/>.
"""

import asyncio
import agenius

import discord
from discord.ext import commands, tasks

from yt_dlp import YoutubeDL as yt_dlp
from shortcuts import misc

ytdl_opts = {'format': 'bestaudio/audio', "quiet": True, "ignoreerrors": True}
ffmpeg_opts = '-vn'


class Music(commands.Cog, name="Music", description="Music commands"):
    def __init__(self, bot):
        self.logger = bot.logger
        self.bot = bot
        self.checks = 0
        self.genius = agenius.Genius(self.bot.config["genius_token"])

        self.music_queue = []
        self.queue_index = 0
        self.ctx = {}

    def add_to_queue(self, songs, ctx):
        """
        Adds the song(s) to the queue.

        :param songs: dict, the songs
        :param ctx: class, the context

        :return: dict, the last song added to the queue
        """
        for song in songs["entries"]:
            if song is None:
                pass
            else:
                info = {
                    "hls": song["url"],
                    "url": song["original_url"],
                    "title": song["title"],
                    "artist": song["uploader"],
                    "length": int(song["duration"])
                }
                self.music_queue.append([info, ctx.guild.voice_client, ctx.author])
                self.logger.log("info", "play", f"Added {info['title']} to the queue")

        return song

    def search(self, video, arg):
        """
        Search and find a video based on keywords or url.

        :param video: str, keyword/url that it searches for
        :param arg: str, platform to search

        :return: dict, dictionary with results
        """
        self.logger.log("info", "search", f"Searching for '{video}' with '{arg}'..")
        with yt_dlp(ytdl_opts) as yt_l:
            if video.startswith("https://"):
                info = yt_l.extract_info(video, download=False)
                if len(info["entries"]) < 1:
                    raise ValueError("Search result returned nothing")
                self.logger.log("info", "search", f"Playlist ({info['webpage_url']})")
            else:
                # info = yt_l.extract_info(f"ytsearch:{video}", download=False)["entries"][0]
                info = yt_l.extract_info(f"{arg}{video}", download=False)
                if len(info["entries"]) < 1:
                    raise ValueError("Search result returned nothing")
                self.logger.log("info", "search", f"Found '{info['title']}' ({info['entries'][0]['display_id']})")
        result = info
        if len(result["entries"]) > 50:
            raise ValueError("You shouldn't queue more than 50 videos at the same time.")

        return result

    def add_attachment_to_queue(self, files, ctx):
        """
        Adds the file(s) to the queue.

        :param files:  list[discord.Attachment], the files
        :param ctx:  discord.Context, the context

        :return:  dict, the last fjle added to the queue
        """

        for file in files:
            if "audio" not in file.content_type:
                raise self.bot.errors.BadAttachment("Attachment isn't an audio file")
            # check length via ffprobe
            a = misc.terminal(f"ffprobe {file} -show_entries format=duration -v quiet -of csv=\"p=0\"")
            self.logger.log("info", "attachment_url", f"Got {str(file)}")
            result = {
                "hls": str(file),
                "url": str(file),
                "title": file.filename.replace('_', ' '),
                "artist": "Unknown Artist",
                "length": round(float(a)),
                "keywords": file.filename.split('.')[0].replace('_', ' ')
            }
            self.music_queue.append([result, ctx.guild.voice_client, ctx.author])
            self.logger.log("info", "add_attachment_to_queue", f"Added {result['title']} to the queue")

        return file

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
            await self.ctx[vc.guild.id].send(embed=embed)
            self.logger.log('info', "play_music", f"Sent '{embed.title}' embed")

            self.queue_index += 1

            self.logger.log('info', "play_music", f"Playing '{song['title']}'")
            vc.play(discord.FFmpegPCMAudio(song["hls"], options=ffmpeg_opts),
                    after=lambda play: asyncio.run_coroutine_threadsafe(self.play_music(), self.bot.loop))

    @tasks.loop(minutes=5)
    async def inactivity(self, ctx):
        if not ctx.guild.voice_client.is_playing() or len(ctx.guild.voice_client.channel.members) < 2:
            self.checks += 1
            self.logger.log("warn", "inactivity", f"Inactivity check #{self.checks} returned true")
        else:
            self.logger.log("warn", "inactivity", f"Inactivity check #{self.checks} returned false")
            self.checks = 0

        if self.checks > 3:
            self.music_queue.clear()
            self.queue_index = 0
            await ctx.voice_client.disconnect()
            embed = discord.Embed(title="Inactivity", description="Bot has been inactive for too long, leaving vc",
                                  color=discord.Color.red())
            await ctx.send(embed=embed)
            self.logger.log("warn", "inactivity", "Too much inactivity, left vc")
            self.checks = 0
            self.inactivity.cancel()

    @commands.command(name="join", aliases=['j'], brief="Joins the voice channel")
    async def join(self, ctx):
        voice_client = ctx.guild.voice_client
        author_voice = ctx.author.voice

        if not author_voice:
            raise self.bot.errors.AuthorNotInVoice("Author not in any voice channel")

        vc = author_voice.channel
        if not voice_client:
            await vc.connect()
            self.ctx = {ctx.guild.id: ctx}
            self.logger.log("info", "join", f"Joined {str(ctx.guild) + '/' + str(vc)}")
            await ctx.send(f"Joined `{vc}`!")
            await asyncio.sleep(300)
            self.inactivity.start(ctx)
        else:
            await voice_client.move_to(vc)
            self.logger.log("info", "join", f"Joined {str(ctx.guild) + '/' + str(vc)}")
            await ctx.send(f"Joined `{vc}`!")

    @commands.command(name="play", aliases=['p'], brief="Plays your requested song")
    async def play(self, ctx, *args):
        args = list(args)
        try:
            if args[0].startswith("-"):
                flag = args.pop(0)
            else:
                flag = "--youtube"
        except IndexError:
            raise self.bot.errors.BadArgument("Is an argument that is required but missing", "*args")
        if flag in ('-yt', "--youtube"):
            search_type = "ytsearch:"
        elif flag in ('-sc', "--soundcloud"):
            search_type = "scsearch:"
        else:
            raise self.bot.errors.BadArgument("That flag doesn't exist", flag)
        self.logger.log("info", "play", flag)

        args = " ".join(args)
        voice_client = ctx.guild.voice_client
        vc = ctx.author.voice

        if not vc:
            raise self.bot.errors.AuthorNotInVoice()
        if not voice_client:
            raise self.bot.errors.NoVoiceClient()
        if vc.channel != voice_client.channel:
            raise self.bot.errors.AuthorNotInVoice()

        async with ctx.typing():
            songs = self.search(args, search_type)
            song = self.add_to_queue(songs, ctx)
            self.music_queue[-1][0]["keywords"] = args
            if not args.startswith("https://"):
                await ctx.send(f"Added `{song['title']}` to the queue!")
            else:
                await ctx.send(f"Added `{songs['title']}` to the queue!")

        if not voice_client.is_playing():
            await self.play_music()

    @commands.command(name="queue", aliases=['q'], brief="Shows the queue")
    async def queue(self, ctx):
        if self.music_queue:
            result = misc.queue_format(self.music_queue, self.queue_index)
            await ctx.send(result)
        else:
            await ctx.send("The queue is empty")

    @commands.command(name="playfile", aliases=['pf'], brief="Plays your file")
    async def playfile(self, ctx):
        author_voice = ctx.author.voice
        voice_client = ctx.guild.voice_client

        if not author_voice:
            raise self.bot.errors.AuthorNotInVoice()
        if not voice_client:
            raise self.bot.errors.NoVoiceClient()
        if author_voice.channel != voice_client.channel:
            raise self.bot.errors.AuthorNotInVoice()
        if not ctx.message.attachments:
            raise self.bot.errors.NoAttachment("There are no files attached to your message")

        song = self.add_attachment_to_queue(ctx.message.attachments, ctx)
        if not len(ctx.message.attachments) > 1:
            await ctx.send(f"Added {song.filename} to the queue!")
        else:
            await ctx.send("Added the songs to the queue!")

        if not voice_client.is_playing():
            await self.play_music()

    @commands.command(name="pause", brief="Pauses/resumes the current song")
    async def pausing(self, ctx):
        voice_client = ctx.guild.voice_client
        author_voice_client = ctx.author.voice

        if not voice_client:
            raise self.bot.errors.NoVoiceClient()
        if author_voice_client.channel != voice_client.channel:
            raise self.bot.errors.AuthorNotInVoice()
        if voice_client.is_playing():
            voice_client.pause()
            await ctx.send("Paused the music")
            self.logger.log("info", "pause", "Paused the music")
        else:
            voice_client.resume()
            await ctx.send("Resumed the music")
            self.logger.log("info", "pause", "Resumed the music")

    @commands.command(name="skip", brief="Skips the current song and goes to the next one")
    async def skip(self, ctx):
        voice_client = ctx.guild.voice_client
        author_voice_client = ctx.author.voice

        if not voice_client:
            raise self.bot.errors.NoVoiceClient()
        if not author_voice_client:
            raise self.bot.errors.AuthorNotInVoice()
        if author_voice_client.channel != voice_client.channel:
            raise self.bot.errors.AuthorNotInVoice()
        if not self.music_queue or len(self.music_queue) < self.queue_index:
            raise self.bot.errors.EmptyQueue("You've reached the end of the queue")

        voice_client.stop()
        await ctx.send("Skipped the song")

    @commands.command(name="stop", brief="Stops the music and clears the queue")
    async def stopping(self, ctx):
        voice_client = ctx.guild.voice_client
        author_voice_client = ctx.author.voice

        if not voice_client:
            raise self.bot.errors.NoVoiceClient("Bot not in any voice channel")
        if author_voice_client.channel != voice_client.channel:
            raise self.bot.errors.AuthorNotInVoice()
        if not voice_client.is_playing():
            await ctx.send("There's nothing playing")
        else:
            self.music_queue.clear()
            self.queue_index = 0
            voice_client.stop()
            await ctx.send("Stopped the music")

    @commands.command(name="leave", aliases=["disconnect", 'd'], brief="Leaves the voice channel")
    async def leave(self, ctx):
        voice_client = ctx.guild.voice_client
        author_voice_client = ctx.author.voice

        if not author_voice_client:
            raise self.bot.errors.AuthorNotInVoice()
        if not voice_client:
            raise self.bot.errors.NoVoiceClient()
        if author_voice_client.channel != voice_client.channel:
            raise self.bot.errors.AuthorNotInVoice("Author not in same voice channel as bot")

        self.music_queue.clear()
        self.queue_index = 0
        await voice_client.disconnect()
        self.inactivity.cancel()
        await ctx.send("Left voice channel")

    @commands.command(name="remove", aliases=['r'], brief="Removes an item from the queue")
    async def remove(self, ctx, index: int):
        if not 1 < index <= len(self.music_queue):
            raise IndexError("Index out of range")

        await ctx.send(f"Removed `{self.music_queue.pop(index - 1)[0]['title']}` from the queue")

    @commands.command(name="lyrics", aliases=['l'], brief="Searches for the currently playing lyrics")
    async def lyrics(self, ctx):
        assert ctx.guild.voice_client, "Bot not in vc"
        if not ctx.guild.voice_client.is_playing:
            raise self.bot.errors.VoiceClientError("voice_client isn't playing anything")

        song = self.music_queue[self.queue_index - 1][0]
        async with ctx.typing():
            info = await self.genius.search_song(song["keywords"])

        embed = discord.Embed(
            title=info.full_title,
            description=info.lyrics[:2000].split("Lyrics")[1],
            color=discord.Color.random()
        )
        embed.add_field(
            name="\u200b",
            value=info.lyrics[2000:3000].replace("Embed", '') + '…',
            inline=False
        )
        if len(info.lyrics) > 3000:
            embed.add_field(
                name="Character limit hit",
                value=f"Go to {info.url} for the rest",
                inline=False
            )
        embed.set_footer(text="Powered by Genius.com and AGenius.py")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Music(bot))
