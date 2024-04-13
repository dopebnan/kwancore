"""
kwanCore, a discord.py bot foundation.
Copyright (C) 2022  dopebnan

You should have received a copy of the GNU General Public License
along with kwanCore. If not, see <https://www.gnu.org/licenses/>.
"""

import asyncpraw

from discord.ext import commands
import discord


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

    async def get_post_embed(self, subreddit, color=None, timeout=10):
        """
        Get a random image from a subreddit

        :param subreddit:  str, the subreddit name
        :param color:  int, the embed color
            Default: None
        :param timeout:  int, the amount of loops it should do before stopping;
            Default:  10
        """
        subreddit = await self.reddit.subreddit(subreddit)
        submission = await subreddit.random()
        i = 0

        while not submission.post_hint == "image":
            if i >= timeout:
                raise TimeoutError("Couldn't find an image")
            # if 10 posts didn't have an image, then that's worrying
            i += 1
            submission = await subreddit.random()

        self.logger.log("info", "get_post_embed",
                        f"Found {submission.permalink} from r/{submission.subreddit}")
        embed = discord.Embed(
            title=submission.title,
            url=submission.url,
            color=color
        )
        embed.set_image(url=submission.url)
        embed.add_field(name=f":arrow_up: {submission.score} :arrow_down:", value="\u200b")
        embed.set_footer(text=f"Posted by u/{submission.author} in r/{submission.subreddit}")
        return embed

    @commands.command(name="random_image", brief="Gets a random image post from a subreddit")
    async def random_image(self, ctx, subreddit):
        async with ctx.typing():
            embed = await self.get_post_embed(subreddit, discord.Color.random())
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Memes(bot))
