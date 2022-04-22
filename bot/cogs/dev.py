"""
kwancore, an extensive discord.py bot template
Copyright (C) 2022  dopebnan
"""
import os
from platform import platform, python_version
from bot.shortcuts import terminal

import discord
from discord.ext import commands
from discord.utils import get


class Dev(commands.Cog, name="Developer Commands", description="Commands that are for the bot devs and maintainers"):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
        self.config = bot.config

    async def cog_check(self, ctx):
        dev_role = get(ctx.guild.roles, name=self.bot.config["dev_role"])
        return dev_role in ctx.author.roles

    @commands.command(name="stats")
    async def stats(self, ctx):
        pic_num = str(len(os.listdir("assets/images/")))
        header = f"{self.bot.user.name}@[kwanCore]"
        latest_ver = terminal("git tag -l").split('\n')[0]
        try:
            temp = terminal("vcgencmd measure_temp").split('=')[1]
        except IndexError:
            self.logger.log("warn", "stats", "Couldn't measure CPU temp, are you sure this is a raspberrypi?")
            temp = 0
        result = (f"```yaml\n"
                  f"{header}\n{'-' * len(header)}\n"
                  f"OS: {platform().split('-', 1)[0]}\n"
                  f"CPU: {temp}\n"
                  f"Uptime: {terminal(b'uptime -p').replace('up ', '')}"
                  f"Python: {python_version()}\n"
                  f"Discord.py: {discord.__version__}\n"
                  f"Current Version: {self.bot.config['version']}\n"
                  f"Latest Version: {latest_ver}\n"
                  f"Pics: {pic_num}\n"
                  f"```")
        await ctx.send(result)


def setup(bot):
    bot.add_cog(Dev(bot))
