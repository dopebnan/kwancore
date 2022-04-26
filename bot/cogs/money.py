import json

import discord
from discord.ext import commands

with open("usercontent/profiles.json") as file:
    profiles = json.load(file)


class Money(commands.Cog, name="Money", description="Money and stuff"):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
        self.config = bot.config
        self.settings = bot.settings

    @commands.command(name="money_start", brief="Add yourself to the Money experience")
    async def money_start(self, ctx):
        if str(ctx.author.id) in profiles:
            raise self.bot.errors.ProfileAlreadyExists(ctx.author.name)
        user = {
            "Name": ctx.author.name,
            "Level": 1,
            "XP": 1,
            "Coins": {
                "Wallet": 500,
                "Bank": 0,
                "Percentage": 100
            },
            "Inventory": [],
            "Deaths": 0
        }
        profiles[ctx.author.id] = user
        with open("usercontent/profiles.json", 'w') as f:
            json.dump(profiles, f, indent=4)

        await ctx.send("You have entered the Money experience! Have fun!")


def setup(bot):
    bot.add_cog(Money(bot))
