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

import os
import random
import time
import unicodedata
import yaml
import json
import traceback

from shortcuts import easylogger, misc
import embeds, errors

import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot

if not os.path.isdir("logs"):
    os.mkdir("logs/")
if not os.path.isdir("traceback"):
    os.mkdir("traceback/")

easylogger.add_level("command", 21)
logger = easylogger.Logger("logs/log.txt", "$time $cwfile: [$level] $arg: $message")


def default_settings():
    with open("assets/settings.json", 'w') as f:
        json.dump(config["default_settings"], f)
    with open("assets/settings.json") as f:
        sttngs = json.load(f)
    logger.log("info", "initialization/default_settings", "Created a default config.json")
    return sttngs


try:
    with open("assets/config.yaml") as file:
        config = yaml.safe_load(file)
        logger.log("info", "initialization", f"loaded {file.name}")
except FileNotFoundError:
    logger.log("critical", "initialization", "config file not found, stopping..")
    raise FileNotFoundError("Config file not found.")

try:
    with open("assets/settings.json") as file:
        settings = json.load(file)
        logger.log("info", "initialization", f"loaded {file.name}")
except FileNotFoundError:
    logger.log("warn", "initialization", "Couldn't find settings file, creating a default one..")
    settings = default_settings()
except json.decoder.JSONDecodeError:
    logger.log("warn", "initialization", "Couldn't decode the file, are you sure it's not empty? Defaulting..")
    settings = default_settings()
if len(settings) != len(config["default_settings"]):
    logger.log("error", "initialization", f"Bad settings file, defaulting..")
    settings = default_settings()

status_msg = ["KWANCORE!!!", "kc!"]

bot = Bot(command_prefix="kc!")

bot.config = config
bot.logger = logger
bot.errors = errors
bot.descriptions = {
    "play": ("`kc!play flag *song`\n\nThe bot will search for your requested song and play the best result\n"
             "\nSearch flags:"
             f"\n` -yt, --youtube{' ' * 14}search on youtube`"
             f"\n` -sc, --soundcloud{' ' * 11}search on soundcloud`"),
    "playfile": "`kc!playfile`\n\nThe bot will play the file attached to your message",
    "remove": "`kc!remove index`\n\nRemoves the `index`th item from the queue",
    "settings": ("`kc!settings key value`\n"
                 "\n`key` is the setting you want to change"
                 "\n`value` is what you will change it to\n"
                 "\neg. `kc!settings pic_cooldown 10`")
}
bot.temp_warning = 0


@bot.event
async def on_ready():
    logger.log()
    logger.log(message="kwancore".center(79))
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
        reload()

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
        reload()

bot.remove_command("help")
if __name__ == "__main__":
    pass

for cog in os.listdir("cogs"):
    if cog.endswith(".py"):
        bot.load_extension(f"cogs.{cog.split('.', 1)[0]}")
        logger.log("INFO", "cog loader", f"loaded '{cog}'")


def reload():
    for cogs in os.listdir("cogs"):
        if cogs.endswith(".py"):
            bot.reload_extension(f"cogs.{cogs.split('.', 1)[0]}")
            logger.log("INFO", "reload", f"reloaded '{cogs}'")


@bot.event
async def on_command_completion(ctx):
    logger.log("command", f"{str(ctx.guild) + '/#' + ctx.channel.name}",
               ctx.message.content, f"<{ctx.message.author}, {ctx.message.author.id}>")
    if ctx.command.qualified_name == "settings":
        reload()


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
        err_id = misc.save_traceback(error)
        error_embed_parts = error_message.split(':', 1)
        embed = discord.Embed(title=error_embed_parts[0], description=error_embed_parts[1], color=0xE3170A)
        embed.set_footer(text=f"Error ID: {err_id}")

    await ctx.send(embed=embed)
    logger.log("error", ctx.message.content, error_message,
               f"<{ctx.message.author}, {ctx.message.author.id}>")

    # raise error


bot.run(config["token"])
