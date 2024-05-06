"""
kwanCore, a discord.py bot foundation.
Copyright (C) 2022  dopebnan

You should have received a copy of the GNU General Public License
along with kwanCore. If not, see <https://www.gnu.org/licenses/>.
"""

import discord
from discord.ext import commands

descriptions = {
    "play": ("`$PREFplay [flag] [*song]`\n\nSearches for your requested song and play the best result\n"
             "\nSearch flags:"
             f"\n` -yt, --youtube{' ' * 7}search on youtube`"
             f"\n` -sc, --soundcloud{' ' * 4}search on soundcloud`"),
    "playfile": "`$PREFplayfile`\n\nPlays the file attached to your message",
    "remove": "`$PREFremove [index]`\n\nRemoves the `index`th item from the queue",
    "settings": ("`$PREFsettings [key] [value]`\n"
                 "`$PREFsettings [mode]`\n"
                 "`$PREFsettings`\n"
                 "\nChange the value of each `key` to `value`"
                 "\neg. `$PREFsettings pic_cooldown 10`\n"
                 "\nModes:\n"
                 "`$PREFsettings reset    resets every settings to the default value`\n"
                 "`$PREFsettings          displays the settings`"),
    "update": ("`$PREFupdate [flag]`\n"
               "\nUse the `--help` flag for help"),
    "log": ("`$PREFlog [flag]`\n"
            "\nIf no flags are present, DMs you the log\n"
            "\nFlags:\n"
            "` -n, --create-new    creates a new log.txt, and saves the old one`"),
    "random_image": ("`$PREFrandom_image [subreddit]`\n"
                     "\nGets a random image from r/`subreddit`"),
    "help": ("`$PREFhelp [command]\n"
             "`$PREFhelp`\n"
             "\nDisplays help about a command. If no command is specified then it lists all the commands.")
}


class Help(commands.Cog, name="Help", description="Help commands"):
    def __init__(self, bot):
        Help.color = 0x5de7b4
        self.bot = bot
        self.logger = bot.logger
        self.pref = bot.command_prefix

    @commands.command(name="help", brief="Sends the help message")
    async def help(self, ctx, arg=None):
        if not arg:
            result = "```bash\n"
            for cog in self.bot.cogs:
                cog = self.bot.get_cog(cog)
                result += f"{cog.qualified_name}\n# {cog.description}\n"
                self.logger.log("info", "help",
                                f"Set-up the core of '{cog.qualified_name}' msg")
                coms = cog.get_commands()
                for cmd in coms:
                    result += f"{cmd.name}{' ' * (14 - len(cmd.name))}- {cmd.brief}\n"
                    self.logger.log("info", "help",
                                    f"Added '{cmd.qualified_name}' to the msg")
                result += "\n\n"

            result += ("You can also search for a specific command by putting the command name at the end!\n"
                       "```")
            await ctx.send(result)
            self.logger.log("info", "help", "sent msg")
        else:
            if arg not in self.bot.all_commands:
                raise self.bot.errors.BadArgument("That command doesn't exist", arg)

            cmds = self.bot.all_commands
            if arg in descriptions:
                title = descriptions[arg].split("\n\n", 1)[0].replace("$PREF", self.pref)
                desc = descriptions[arg].split("\n\n", 1)[1].replace("$PREF", self.pref)
            else:
                title = f"`{self.bot.command_prefix}{arg}`"
                desc = cmds[arg].brief

            embed = discord.Embed(
                title=title,
                description=desc,
                color=discord.Color.random()
            )
            self.logger.log("info", "help_cb", f"Created {arg} help embed")
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))
