"""
kwanCore, a discord.py bot foundation.
Copyright (C) 2022  dopebnan

You should have received a copy of the GNU General Public License
along with kwanCore. If not, see <https://www.gnu.org/licenses/>.
"""

import aiohttp
import asyncpraw

from discord.ext import commands


async def is_pic(url):
    async with aiohttp.ClientSession() as session:
        async with session.head(url) as r:
            return str(r.headers.get("Content-Type")).startswith("image/")


class Memes(commands.Cog, name="Memes", description="Reddit and stuff"):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
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
            i = 0
            while not await is_pic(submission.url):
                if i >= 10:
                    raise TimeoutError("Couldn't find an image")
                # if 10 posts didn't have an image, then that's worrying
                i += 1
                submission = await subreddit.random()
            await ctx.send(submission.url)


def setup(bot):
    bot.add_cog(Memes(bot))
