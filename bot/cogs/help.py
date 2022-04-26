import discord
from discord.ext import commands

descriptions = {
    "play": ("`kc!play [flag] [*song]`\n\nThe bot will search for your requested song and play the best result\n"
             "\nSearch flags:"
             f"\n` -yt, --youtube{' ' * 7}search on youtube`"
             f"\n` -sc, --soundcloud{' ' * 4}search on soundcloud`"),
    "playfile": "`kc!playfile`\n\nThe bot will play the file attached to your message",
    "remove": "`kc!remove [index]`\n\nRemoves the `index`th item from the queue",
    "settings": ("`kc!settings [key] [value]`\n"
                 "`kc!settings [mode]`\n"
                 "\nChange the value of each `key` to `value`"
                 "\neg. `kc!settings pic_cooldown 10`\n"
                 "\nModes:\n"
                 "`kc!settings reset    resets every settings to the default value`\n"
                 "`kc!settings          displays the settings`"),
    "update": ("`kc!update [flag]`\n"
               "\nUse the `--help` flag for help"),
    "log": ("`kc!log [flag]`\n"
            "\nIf no flags are present, DMs you the log\n"
            "\nFlags:\n"
            "` -n, --create-new    creates a new log.txt, and saves the old one`"),
    "random_image": ("`kc!random_image [subreddit]`\n"
                     "\nGets a random image from r/`subreddit`")
}


class Help(commands.Cog, name="Help", description="Help commands"):
    def __init__(self, bot):
        Help.color = 0x5de7b4
        self.bot = bot
        self.logger = bot.logger

    @commands.command(name="help", brief="Help message")
    async def help(self, ctx, arg=None):
        if not arg:
            result = "```bash\n"
            for cog in self.bot.cogs:
                result += f"{cog}\n# {self.bot.cogs[cog].description}\n"
                self.logger.log("info", "help", f"Set-up the core of '{cog}' msg")
                for cmd in self.bot.commands:
                    if cmd.cog == self.bot.cogs[cog]:
                        result += f"{cmd.name}{' '* (12 - len(cmd.name))}- {cmd.brief}\n"
                        self.logger.log("info", "help", f"Added '{cmd.qualified_name}' to the msg")
                result += "\n\n"

            result += "You can also search for a specific command by putting the command name at the end!\n```"
            await ctx.send(result)
            self.logger.log("info", "help", "sent msg")
        else:
            if arg not in self.bot.all_commands:
                raise self.bot.errors.BadArgument("That command doesn't exist", arg)
            else:
                cmds = self.bot.all_commands
                if arg in descriptions:
                    title = descriptions[arg].split("\n\n", 1)[0]
                    desc = descriptions[arg].split("\n\n", 1)[1]
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


def setup(bot):
    bot.add_cog(Help(bot))
