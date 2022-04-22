"""
kwancore, an extensive discord.py bot template
Copyright (C) 2022  dopebnan
"""
import os
from platform import platform, python_version
from shortcuts import terminal

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

    @commands.command(name="sysinfo", brief="Display system information")
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

    @commands.command(name="update")
    async def update(self, ctx, flag="-m"):
        status = terminal("cd ../ && git fetch && git status").split('\n', 3)[1]
        h = False
        if flag == '-h' or flag == "--help":
            msg = ("```bash\n"
                   "kc!update [mode]\n"
                   "Update or reset the bot\n"
                   "Modes:\n"
                   f" -r, --reset{' ' * 17}delete changes and revert back to the original commit\n"
                   f" --hard-pull{' ' * 17}delete changes and update to the latest commit\n"
                   f" -m, --merge{' ' * 17}save changes and update to the latest commit\n"
                   f" -h, --help{' ' * 18}display this help message and exit"
                   f"```"
                   )
            h = True
            await ctx.send(msg)

        elif flag == '-r' or flag == "--reset":
            await ctx.send("This will reset the current version to the specified commit.\n"
                           "Do you want to continue? [Y/n]")
            cmd = "cd ../ && git reset --hard"
        elif flag == '--hard-pull':
            await ctx.send("This will reset the current version and update to the latest commit.\n"
                           "Do you want to continue? [Y/n]")
            cmd = "cd ../ && git reset --hard && git pull --no-stat"
        elif flag == '-m' or flag == "--merge":
            await ctx.send("This will join the current version with the latest commit.\n"
                           "Do you want to continue? [Y/n]")
            cmd = "cd ../ && git merge --no-commit --no-stat -v"
        else:
            raise self.bot.errors.BadArgument(flag, "That flag doesn't exist.")

        if not h:
            def check(m):
                return m.author == ctx.author

            msg = await self.bot.wait_for('message', check=check, timeout=30)

            if msg.content.lower() == 'y':
                pull = terminal(cmd)
                await ctx.send(f"{pull}.")
            else:
                await ctx.send("Aborted.")


def setup(bot):
    bot.add_cog(Dev(bot))
