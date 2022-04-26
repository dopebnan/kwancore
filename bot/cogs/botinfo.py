"""
kwancore, an extensive discord.py bot template
Copyright (C) 2022  dopebnan
"""
import discord
from discord.ext import commands


class BotInfo(commands.Cog, name="Bot Info", description="Stuff about the bot"):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
        self.config = bot.config

    @commands.command(name="changelog", aliases=["changes", "updates"], brief="Sends the changelog")
    async def info(self, ctx):
        file = discord.File('../changelog.md')
        await ctx.send(file=file)

    @commands.command(name="info", brief="Information about the bot")
    async def info(self, ctx):
        embed = discord.Embed(
            title="Info",
            color=0x5de7b4
        )
        embed.add_field(
            name="kwancore Creator:",
            value="dopebnan",
            inline=False
        )
        embed.add_field(
            name="Version:",
            value=f"{self.bot.version}",
            inline=True
        )
        await ctx.send(embed=embed)

    @commands.command(name="ping", brief="Check the latency")
    async def ping(self, ctx):
        msg = f"The ping is {round(self.bot.latency * 1000)}ms"
        await ctx.send(msg)

    @commands.command(name="report", brief="Report a bug or a feature")
    async def report(self, ctx):
        embed = discord.Embed(
            title="Report",
            description="You should open an [issue](https://github.com/dopebnan/kwancore/issues)!",
            color=0x5de7b4
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(BotInfo(bot))
