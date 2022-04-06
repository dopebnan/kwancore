import discord
from discord.ext import commands


class Help(commands.Cog, name="Help", description="Help commands"):
    def __init__(self, bot):
        Help.color = 0x5de7b4
        self.logger = bot.logger
        self.bot = bot

    @commands.command(name="help", brief="Help message in multi-embed format")
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
            self.logger.log("info", "help", f"sent {embed.title} embed.")

    @commands.command(name="help_btk", brief="Help message in codeblock format")
    async def help_btk(self, ctx):
        result = "```\n"
        for cog in self.bot.cogs:
            result += f"{cog}\n#{self.bot.cogs[cog].description}\n\n"
            self.logger.log("info", "help", f"Set-up the core of '{cog}' msg")
            for cmd in self.bot.commands:
                if cmd.cog == self.bot.cogs[cog]:
                    result += f"{cmd.name} - {cmd.brief}\n"
                    self.logger.log("info", "help", f"Added '{cmd.qualified_name}' to the msg")
            result += "\n\n"

        result += "```"
        await ctx.send(result)
        self.logger.log("info", "help", "sent msg")

    @commands.command(name="help_oe", brief="Help message in one embed format")
    async def help_oe(self, ctx):
        embed = discord.Embed(
            title="Help",
            color=discord.Color.random()
        )
        self.logger.log("info", "help_oe", "Set up the main help embed")
        for cog in self.bot.cogs:
            embed.add_field(
                name=f"{cog}",
                value=self.bot.cogs[cog].description,
                inline=False
            )

            self.logger.log("info", "help_oe", f"Added {cog} field")

            for cmd in self.bot.commands:
                if cmd.cog == self.bot.cogs[cog]:
                    embed.add_field(
                        name=self.bot.command_prefix + cmd.name,
                        value=cmd.brief,
                    )
                    self.logger.log("info", "help_oe", f"Added '{cmd.qualified_name}' to the embed")
            embed.add_field(name=u"\u200b", value=u"\u200b", inline=False)
        embed.remove_field(-1)
        await ctx.send(embed=embed)

        self.logger.log("info", "help_oe", f"Sent help embed.")


def setup(bot):
    bot.add_cog(Help(bot))
