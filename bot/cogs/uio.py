"""
kwancore, an extensive discord.py bot template
Copyright (C) 2022  dopebnan
"""
import json

import discord
from discord.ext import commands
from discord.ext.commands import BucketType

with open("assets/settings.json") as file:
    settings = json.load(file)


class UIO(commands.Cog, name="UserInput/Output", description="General I/O commands"):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger

    @commands.command(name="pic", brief="Sends a picture.")
    @commands.cooldown(1, settings["pic_cooldown"], BucketType.user)
    async def pic(self, ctx):
        img = "assets/images/kwancore.png"
        await ctx.send(file=discord.File(img))

        if settings["pic_cooldown_bool"]:
            await ctx.send(f"*Cooldown has been set to **{settings['pic_cooldown']}s***")
        self.logger.log("info", "pic", f"Sent {img} to {ctx.channel}")

    @commands.command(name="echo", brief="Echoes your message.")
    @commands.cooldown(1, settings["echo_cooldown"], BucketType.user)
    async def echo(self, ctx, msg):
        await ctx.send(msg)


def setup(bot):
    bot.add_cog(UIO(bot))
