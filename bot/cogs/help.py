import discord
from discord.ext import commands


class Help(commands.Cog, name="help", description="Help commands"):
    def __init__(self, bot):
        Help.color = 0x5de7b4
        self.logger = bot.module_el.Logger("logs/log.txt", "$time $cwfile: [$level] $arg: $message", cwf=__file__)
        self.bot = bot

    @commands.command(name="help", brief="Shows this message")
    async def help(self, ctx):

        for cog in self.bot.cogs:
            embed = discord.Embed(
                title=f"{cog}",
                description=self.bot.cogs[cog].description,
                color=self.bot.cogs[cog].color
            )
            self.logger.log("info", "help", f"Set-up the core of '{cog}' embed")
            for cmd in self.bot.commands:
                if cmd.cog == self.bot.cogs[cog]:
                    embed.add_field(
                        name=cmd.name,
                        value=cmd.brief,
                    )
                    self.logger.log("info", "help", f"Added '{cmd.qualified_name}' to the embed")
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
