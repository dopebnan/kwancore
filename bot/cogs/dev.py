"""
kwanCore, a discord.py bot foundation.
Copyright (C) 2022  dopebnan

You should have received a copy of the GNU General Public License
along with kwanCore. If not, see <https://www.gnu.org/licenses/>.
"""

import json
import os
import time

import discord
from discord.ext import commands
from discord.utils import get

from shortcuts import terminal

with open("usercontent/settings.json") as file:
    setting = json.load(file)


def is_bool(arg):
    if arg.lower() in ("yes", "y", "true", "1", "enable", "on"):
        return True
    if arg.lower() in ("no", "n", "false", "0", "disable", "off"):
        return False
    raise TypeError("Value isn't a boolean")


class Dev(commands.Cog, name="Developer Commands", description="Commands that are for the bot devs and admins"):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
        self.config = bot.config
        self.setting = setting

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

    @commands.command(name="update", brief="Updates the bot, or resets it to the last.")
    async def update(self, ctx, flag="-m"):
        status = terminal("cd ../ && git fetch && git status").split('\n', 3)[1]
        cmd = ''
        h = False
        if flag in ('-h', "--help"):
            msg = ("```bat\n"
                   f"{self.bot.command_prefix}update [mode]\n"
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

        elif flag in ('-r', "--reset"):
            await ctx.send("This will reset the current version to the specified commit.\n"
                           "Do you want to continue? [Y/n]")
            cmd = "cd ../ && git reset --hard"
        elif flag == '--hard-pull':
            await ctx.send(f"{status}\nThis will reset the current version and update to the latest commit.\n"
                           "Do you want to continue? [Y/n]")
            cmd = "cd ../ && git reset --hard && git pull --no-stat"
        elif flag in ('-m', "--merge"):
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
                self.bot.logger.log('INFO', "update", "Restarting...")
                os.execv("./main.py", ("./main.py",))
            else:
                await ctx.send("Aborted.")

    @commands.command(name="settings", brief="Changes the settings")
    async def settings(self, ctx, *args: str):
        if len(args) == 1:
            if args == ("reset",):
                with open("usercontent/settings.json", 'w') as f:
                    self.setting = self.config["default_settings"]
                    json.dump(self.setting, f, indent=2)
                    self.logger.log("info", "settings/reset", "Reset the settings")
            else:
                raise ValueError("There's no value given.")
        elif len(args) > 1:
            if args[0] not in self.setting:
                raise KeyError("That setting doesn't exist.")
            self.setting[args[0]] = int(args[1]) if not args[0].endswith("bool") else is_bool(args[1])
            with open("usercontent/settings.json", 'w') as f:
                json.dump(self.setting, f)
            self.logger.log("info", "settings/change", f"Changed {args[0]} to {args[1]}.")

        embed = discord.Embed(
            title="Settings",
            color=discord.Color.gold()
        )
        self.logger.log("info", "settings", "Set up core of settings embed.")

        for setting in self.setting:
            embed.add_field(
                name=str(setting),
                value=str(self.setting[setting])
            )
            self.logger.log("info", "settings", f"Added '{setting}' field to settings embed")

        await ctx.send(embed=embed)
        self.logger.log("info", "settings", "Sent settings embed")

    @commands.command(name="log", brief="DMs you the log file")
    async def log(self, ctx, arg=None):
        if not arg:
            user = ctx.message.author
            log = discord.File("./logs/log.txt")
            await user.send("The log file", file=log)
            await ctx.send("Check DMs")
        elif arg in ('-n', "--create-new"):
            os.rename("./logs/log.txt", f"./logs/log{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}")
            self.logger.log("info", "log/arg_n", "Created a new log file.")
            await ctx.send("Created a new log file")


def setup(bot):
    bot.add_cog(Dev(bot))
