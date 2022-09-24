#!/usr/bin/env python3

"""
kwanCore, a discord.py bot foundation.
Copyright (C) 2022  dopebnan

This file is part of kwanCore.

kwanCore is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

KwanCore is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with kwanCore. If not, see <https://www.gnu.org/licenses/>.
"""

import os
import random
import unicodedata
import json
import yaml
import asyncio

import discord
from discord.ext import commands, tasks

import shortcuts
import embeds
import errors

if not os.path.isdir("logs"):
    os.mkdir("logs/")
if not os.path.isdir("traceback"):
    os.mkdir("traceback/")


logger = shortcuts.Logger("logs/log.txt", "$time $cwfile: [$level] $arg: $message")
logger.add_level("command", 21)


def default_settings():
    """Makes a default settings.json"""
    with open("usercontent/settings.json", 'w') as f:
        json.dump(config["default_settings"], f, indent=2)
    with open("usercontent/settings.json") as f:
        logger.log("info", "initialization/default_settings", "Created a default settings.json")
        return json.load(f)


try:
    with open("usercontent/config.yaml") as file:
        config = yaml.safe_load(file)
        logger.log("info", "initialization", f"loaded {file.name}")
except FileNotFoundError:
    logger.log("critical", "initialization", "config file not found, stopping..")
    raise FileNotFoundError("Config file not found.")

try:
    with open("usercontent/settings.json") as file:
        settings = json.load(file)
        logger.log("info", "initialization", f"loaded {file.name}")
except FileNotFoundError:
    logger.log("warn", "initialization", "Couldn't find settings file, creating a default one..")
    settings = default_settings()
except json.decoder.JSONDecodeError:
    logger.log("warn", "initialization", "Couldn't decode the file, are you sure it's not empty? Defaulting..")
    settings = default_settings()
if len(settings) != len(config["default_settings"]):
    logger.log("error", "initialization", "Bad settings file, defaulting..")
    settings = default_settings()

status_msg = ["KWANCORE!!!", "kc!"]


class KwanCore(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        self.logger = logger
        self.errors = errors
        self.version = "1.0.2-beta"
        self.temp_warning = 0

    async def setup_hook(self):
        self.status_task.start()
        self.temp_task.start()

        self.remove_command("help")

        for cog in os.listdir("cogs"):
            if cog.endswith(".py"):
                await self.load_extension(f"cogs.{cog.split('.', 1)[0]}")

    async def on_ready(self):
        logger.log()
        logger.log(message="kwancore".center(30))
        logger.log(message=f"discord.py version: {discord.__version__}".center(30))
        logger.log(message=f"bot: {self.user.name}".center(30))
        logger.log()

    def reload(self):
        for cogs in os.listdir("cogs"):
            if cogs.endswith(".py"):
                self.reload_extension(f"cogs.{cogs.split('.', 1)[0]}")
                logger.log("INFO", "reload", f"Reloaded '{cogs}'")

    @tasks.loop(minutes=10)
    async def status_task(self):
        await self.wait_until_ready()
        chosen_status = random.choice(status_msg)
        await self.change_presence(status=discord.Status.online, activity=discord.Game(chosen_status))
        logger.log("info", "status_task", f"changed status to '{chosen_status}'")

    @tasks.loop(minutes=5)
    async def temp_task(self):
        await self.wait_until_ready()
        try:
            logger.log("info", "temp_task", "trying to get temperature")
            temp = float(shortcuts.terminal("vcgencmd measure_temp").split('=', 1)[1].split("'", 1)[0])
        except IndexError:
            temp = 0
            logger.log("warn", "temp_task", "couldn't get temperature, are you sure this is a raspberrypi?")

        if 80 > temp > 70:
            self.temp_warning += 1
        elif temp < 70:
            self.temp_warning = 0
        else:
            logger.log("critical", "temp_task", f"the cpu reached {temp}'C")
            logger.log("info", "temp_task", "reloading..")
            self.reload()

        if 0 < self.temp_warning < 5:
            embed = discord.Embed(title="WARNING", description=f"the pi's temp is `{temp}'C`", color=0xffc300)
            embed.set_footer(text=f"{self.temp_warning}. warning")
            uptime = shortcuts.terminal('uptime').split(': ')[1][:-1]
            logger.log("warn", "temp_task",
                       f"the cpu reached {temp}'C ({self.temp_warning}) [{uptime}]")

            chan = self.get_channel(config["warningChannel"])
            await chan.send(embed=embed)
            logger.log("info", "temp_task", "sent warning embed")

        elif self.temp_warning > 5:
            self.temp_warning = 0
            embed = discord.Embed(title="STOPPING", description=f"the pi's temp is `{temp}'C`", color=0xcc3300)
            embed.set_footer(text="last warning")
            logger.log("CRITICAL", "temp_task", f"The cpu reached {temp}'C, reloading")

            chan = self.get_channel(config["warningChannel"])
            await chan.send(embed=embed)
            logger.log("info", "temp_task", "sent error embed")

            logger.log("info", "temp_task", "reloading..")
            self.reload()

    async def on_command_completion(self, ctx):
        cmd = ctx.command.qualified_name
        logger.log("command", f"{str(ctx.guild) + '/#' + ctx.channel.name}",
                   ctx.message.content, f"<{ctx.message.author}, {ctx.message.author.id}>")
        if cmd == "settings":
            await self.reload_extension("cogs.uio")
            logger.log("info", "on_command_completion/reload", "reloaded uio.py")

    async def on_message(self, message):
        if message.author == self.user:
            return

        msg = unicodedata.normalize('NFKD', message.content.casefold())

        if 'kwancore' in msg:
            await message.channel.send("kwancore pog!")
            logger.log("info", "on_message", "kwancore in message")

        await self.process_commands(message)

    async def on_command_error(self, ctx, error):
        # cmd = ctx.command.qualified_name if ctx.command else ctx.command
        error_message = str(error).replace("Command raised an exception: ", '')

        if isinstance(error, commands.CommandOnCooldown):
            seconds = round(error.retry_after)
            embed = embeds.command_on_cooldown(seconds)

        elif isinstance(error, commands.CommandNotFound):
            embed = embeds.command_not_found()

        else:
            err_id = shortcuts.save_traceback(error)
            try:
                error_embed_parts = error_message.split(':', 1)
                embed = discord.Embed(title=error_embed_parts[0], description=error_embed_parts[1], color=0xE3170A)
            except IndexError:
                embed = discord.Embed(title="Error:", description=error_message, color=0xE3170A)
            embed.set_footer(text=f"Error ID: {err_id}")

        await ctx.send(embed=embed)
        logger.log("error", ctx.message.content, error_message,
                   f"<{ctx.message.author}, {ctx.message.author.id}>")

        # raise error


async def main():
    async with KwanCore(command_prefix="kc!", intents=discord.Intents.all()) as bot:
        await bot.start(bot.config["token"])


asyncio.run(main())
