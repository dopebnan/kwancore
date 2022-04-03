"""
kwancore, an extensive discord.py bot template
Copyright (C) 2022  dopebnan

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import asyncio
import os
import random
import unicodedata
import yaml

from shortcuts import easylogger, misc
import embeds

import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot

if not os.path.isdir("logs"):
    os.mkdir("logs/")

logger = easylogger.Logger("logs/log.txt", "$time $cwfile: [$level] $arg: $message", cwf=__file__)

with open("assets/config.yml") as file:
    config = yaml.safe_load(file)
    logger.log("info", message="loaded config.yml")

status_msg = ["KWANCORE!!!", "kc!"]

bot = Bot(command_prefix="kc!")

bot.temp_warning = 0


@bot.event
async def on_ready():
    logger.log()
    logger.log(message="kwancore!".center(79))
    logger.log(message=f"discord.py version: {discord.__version__}".center(79))
    logger.log(message=f"bot: {bot.user.name}".center(79))
    logger.log()
    status_task.start()
    logger.log("info", "on_ready", "started status_task")
    temp_task.start()
    logger.log("info", "on_ready", "started temp_task")


@tasks.loop(minutes=10)
async def status_task():
    chosen_status = random.choice(status_msg)
    await bot.change_presence(activity=discord.Game(chosen_status))
    logger.log("info", "status_task", f"changed status to '{chosen_status}'")


@tasks.loop(minutes=5)
async def temp_task():
    await bot.wait_until_ready()
    try:
        logger.log("info", "temp_task", "trying to get temperature")
        temp = float(misc.terminal("vcgencmd measure_temp").split('=', 1)[1].split("'", 1)[0])
    except:
        temp = 0
        logger.log("warn", "temp_task", "couldn't get temperature, are you sure this is a raspberrypi?")

    if 80 > temp > 70:
        bot.temp_warning += 1
    elif temp > 80:
        logger.log("critical", "temp_task", f"the cpu reached {temp}'C")
        logger.log("info", "temp_task", "reloading..")
        await reload()

    if 0 < bot.temp_warning < 5:
        embed = discord.Embed(title="WARNING", description=f"the pi's temp is `{temp}'C`", color=0xffc300)
        embed.set_footer(text=f"{bot.temp_warning}. warning")
        logger.log("warn", "temp_task", f"the cpu reached {temp}'C ({bot.temp_warning})")

        chan = bot.get_channel(config["warningChannel"])
        await chan.send(embed=embed)
        logger.log("info", "temp_task", "sent warning embed")

    elif bot.temp_warning > 5:
        bot.temp_warning = 0
        embed = discord.Embed(title="STOPPING", description=f"the pi's temp is `{temp}'C`", color=0xcc3300)
        embed.set_footer(text=f"last warning")
        logger.log("CRITICAL", "temp_task", f"the cpu reached {temp}'C, reloading")

        chan = bot.get_channel(config["warningChannel"])
        await chan.send(embed=embed)
        logger.log("info", "temp_task", "sent error embed")

        logger.log("info", "temp_task", "reloading..")
        await reload()

if __name__ == "__main__":
    pass

for cog in os.listdir("cogs"):
    if cog.endswith(".py"):
        bot.load_extension(f"cogs.{cog.split('.', 1)[0]}")
        logger.log("INFO", "cog loader", f"loaded '{cog}'")


async def reload():
    await asyncio.sleep(5)  # this is needed incase of an update or lag
    for cogs in os.listdir("cogs"):
        if cogs.endswith(".py"):
            bot.reload_extension(f"cogs.{cogs.split('.', 1)[0]}")
            logger.log("INFO", "reload", f"reloaded '{cogs}'")


@bot.event
async def on_command_completion(ctx):
    logger.log("info", f"<{ctx.message.author}, {ctx.message.author.id}>", ctx.command.qualified_name)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg = unicodedata.normalize('NFKD', message.content.casefold())

    if 'kwancore' in msg:
        await message.channel.send("kwancore pog!")
        logger.log("info", "on_message", "kwancore in message")

    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    cmd = ctx.command.qualified_name if ctx.command else ctx.command
    error_message = str(error).replace("Command raised an exception: ", '')

    if isinstance(error, commands.CommandOnCooldown):
        seconds = round(error.retry_after)
        embed = embeds.command_on_cooldown(seconds)

    elif isinstance(error, commands.CommandNotFound):
        embed = embeds.command_not_found()

    else:
        error_embed_parts = error_message.split(':', 1)
        embed = discord.Embed(title=error_embed_parts[0], description=error_embed_parts[1], color=0xE3170A)
    await ctx.send(embed=embed)
    logger.log("error", f"<{ctx.message.author}, {ctx.message.author.id}>", f"{error_message} ({ctx.message.content})")

    # raise error


bot.run(config["token"])
