"""
kwancore, an extensive discord.py bot template
Copyright (C) 2022  dopebnan
"""
import json
import os
from platform import platform, python_version
from shortcuts import terminal

import discord
from discord.ext import commands
from discord.utils import get


def is_bool(arg):
    if arg.lower() in ("yes", "y", "true", "1", "enable", "on"):
        return True
    elif arg.lower() in ("no", "n", "false", "0", "disable", "off"):
        return False
    else:
        raise TypeError("Value isn't a boolean")


class Dev(commands.Cog, name="Developer Commands", description="Commands that are for the bot devs and maintainers"):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
        self.config = bot.config
        self.settings = bot.settings

    async def cog_check(self, ctx):
        dev_role = get(ctx.guild.roles, name=self.bot.config["dev_role"])
        if dev_role not in ctx.author.roles:
            embed = discord.Embed(
                title="You don't have the developer role.",
                description="That means you don't have access to the developer commands",
                color=discord.Color.dark_red()
            )
            await ctx.send(embed=embed)
        else:
            return True

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

    @commands.command(name="update", brief="Update the bot, or reset it to a commit.")
    async def update(self, ctx, flag="-m"):
        status = terminal("cd ../ && git fetch && git status").split('\n', 3)[1]
        h = False
        if flag == '-h' or flag == "--help":
            msg = ("```bat\n"
                   "kc!update [mode]\n"
                   "Update the bot, or reset it to a commit.\n"
                   "\nModes:\n"
                   f" -r, --reset{' ' * 5}delete changes and revert back to the original commit\n"
                   f" --hard-pull{' ' * 5}delete changes and update to the latest commit\n"
                   f" -m, --merge{' ' * 5}save changes and update to the latest commit\n"
                   f" -h, --help{' ' * 6}display this help message and exit"
                   f"```"
                   )
            h = True
            await ctx.send(msg)

        elif flag == '-r' or flag == "--reset":
            await ctx.send("This will reset the current version to the specified commit.\n"
                           "Do you want to continue? [Y/n]")
            cmd = "cd ../ && git reset --hard"
        elif flag == '--hard-pull':
            await ctx.send(f"{status}\nThis will reset the current version and update to the latest commit.\n"
                           "Do you want to continue? [Y/n]")
            cmd = "cd ../ && git reset --hard && git pull --no-stat"
        elif flag == '-m' or flag == "--merge":
            await ctx.send(f"{status}\nThis will join the current version with the latest commit.\n"
                           "Do you want to continue? [Y/n]")
            cmd = "cd ../ && git merge --no-commit --no-stat -v"
        else:
            raise self.bot.errors.BadArgument("That flag doesn't exist.", flag)

        if not h:
            def check(m):
                return m.author == ctx.author

            msg = await self.bot.wait_for('message', check=check, timeout=30)

            if msg.content.lower() == 'y':
                pull = terminal(cmd)
                status = terminal("cd ../ && git fetch && git status").split('\n', 3)[1]
                await ctx.send(f"{pull}\n{status}")
            else:
                await ctx.send("Aborted.")

    @commands.command(name="settings", brief="Change the settings")
    async def settings(self, ctx, *args: str):
        if len(args) == 1:
            if args == ("reset",):
                with open("assets/settings.json", 'w') as f:
                    self.settings = self.config["default_settings"]
                    json.dump(self.settings, f, indent=2)
                    self.logger.log("info", "settings/reset", "Reset the settings")
            else:
                raise ValueError("There's no value given.")
        elif len(args) > 1:
            if args[0] not in self.settings:
                raise KeyError("That setting doesn't exist.")
            self.settings[args[0]] = int(args[1]) if not args[0].endswith("bool") else is_bool(args[1])
            with open("assets/settings.json", 'w') as f:
                json.dump(self.settings, f)
            self.logger.log("info", "settings/change", f"Changed {args[0]} to {args[1]}.")

        embed = discord.Embed(
            title="Settings",
            color=discord.Color.gold()
        )
        self.logger.log("info", "settings", "Set up core of settings embed.")

        for setting in self.settings:
            embed.add_field(
                name=str(setting),
                value=str(self.settings[setting])
            )
            self.logger.log("info", "settings", f"Added '{setting}' field to settings embed")

        await ctx.send(embed=embed)
        self.logger.log("info", "settings", "Sent settings embed")


def setup(bot):
    bot.add_cog(Dev(bot))
