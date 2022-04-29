import aiohttp
import discord
import asyncpraw
from discord.ext import commands


async def is_pic(url):
    async with aiohttp.ClientSession() as session:
        async with session.head(url) as r:
            return r.headers.get("Content-Type").startswith("image/")


class Memes(commands.Cog, name="Memes", description="Reddit and stuff"):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
        self.config = bot.config
        self.settings = bot.settings
        self.reddit = asyncpraw.Reddit(
            client_id=bot.config["reddit"]['client_id'],
            client_secret=bot.config["reddit"]['client_secret'],
            password=bot.config["reddit"]['password'],
            user_agent=bot.config["reddit"]['user_agent'],
            username=bot.config["reddit"]['username']
        )

    @commands.command(name="random_image", brief="Gets a random image post from a subreddit")
    async def random_image(self, ctx, subreddit):
        async with ctx.typing():
            subreddit = await self.reddit.subreddit(subreddit)
            submission = await subreddit.random()
            while not await is_pic(submission.url):
                submission = await subreddit.random()
            await ctx.send(submission.url)


def setup(bot):
    bot.add_cog(Memes(bot))
