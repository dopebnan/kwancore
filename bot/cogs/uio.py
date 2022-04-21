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

descriptions = {
    "settings": ("`kc!settings key value`\n"
                 "\n`key` is the setting you want to change"
                 "\n`value` is what you will change it to\n"
                 "\neg. `kc!settings pic_cooldown 10`")
}

def is_bool(arg):
    if arg.lower() in ("yes", "y", "true", "1", "enable", "on"):
        return True
    elif arg.lower() in ("no", "n", "false", "0", "disable", "off"):
        return False
    else:
        raise TypeError("Value isn't a boolean")


class UIO(commands.Cog, name="UserInput/Output", description="General I/O commands"):
    def __init__(self, bot):
        UIO.color = discord.Color.random()
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

    @commands.command(name="settings", brief="Change the settings", description=descriptions["settings"])
    async def settings(self, ctx, *args: str):
        if args:
            if len(args) < 2:
                raise ValueError("There's no value given.")
            if args[0] not in settings:
                raise KeyError("That settings doesn't exist.")
            settings[args[0]] = int(args[1]) if not args[0].endswith("bool") else is_bool(args[1])
            with open("assets/settings.json", 'w') as f:
                json.dump(settings, f)
            self.logger.log("info", "settings/change", f"Changed {args[0]} to {args[1]}.")

        embed = discord.Embed(
            title="Settings",
            color=discord.Color.gold()
        )
        self.logger.log("info", "settings", "Set up core of settings embed.")

        for setting in settings:
            embed.add_field(
                name=str(setting),
                value=str(settings[setting])
            )
            self.logger.log("info", "settings", f"Added '{setting}' field to settings embed")

        await ctx.send(embed=embed)
        self.logger.log("info", "settings", "Sent settings embed")


def setup(bot):
    bot.add_cog(UIO(bot))
