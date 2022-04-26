"""
kwancore, an extensive discord.py bot template
Copyright (C) 2022  dopebnan
"""
import json

import discord
from discord.ext import commands
from discord.ext.commands import BucketType

with open("usercontent/settings.json") as file:
    settings = json.load(file)


class UIO(commands.Cog, name="UserInput/Output", description="General I/O commands"):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger

    @commands.command(name="pic", brief="Sends a picture.")
    @commands.cooldown(1, settings["pic_cooldown"], BucketType.user)
    async def pic(self, ctx):
        img = "usercontent/images/kwancore.png"
        await ctx.send(file=discord.File(img))

        if settings["pic_cooldown_bool"]:
            await ctx.send(f"*Cooldown has been set to **{settings['pic_cooldown']}s***")
        self.logger.log("info", "pic", f"Sent {img} to {ctx.channel}")

    @commands.command(name="echo", brief="Echoes your message.")
    @commands.cooldown(1, settings["echo_cooldown"], BucketType.user)
    async def echo(self, ctx, msg):
        await ctx.send(msg)

    @commands.command(name="source_code", brief="Redirects you to the source code.")
    async def source_code(self, ctx):
        embed = discord.Embed(
            title="Source code",
            description="You can find the sourcecode on [GitHub](https://github.com/dopebnan/kwancore)",
            color=discord.Color.random()
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(UIO(bot))
