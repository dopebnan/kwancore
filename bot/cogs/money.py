from pymongo import MongoClient
import sqlite3
import json

import discord
from discord.ext import commands


dbcli = MongoClient()
db = dbcli.money

# try:
#     c.execute("""CREATE TABLE profiles (
#                  id INT, name TEXT, level INT, xp INT, wallet INT, bank INT, percentage INT, inventory BLOB, deaths INT
#                  );""")
# except sqlite3.OperationalError:
#     pass
# try:
#     c.execute("""CREATE TABLE "items" (
#                  id INT UNIQUE, emoji TEXT, name TEXT, desc TEXT, description TEXT, price INT, trade_val INT,
#                  type TEXT, rarity TEXT, bundle TEXT,
#                  PRIMARY KEY("id")
#              );""")
#     c.execute("INSERT INTO items VALUES (0, ':black_large_square:', 'nothing', 'it\'s nothing', 'it\'s nothing',"
#               "0, 0, 'None', 'common', 'starters')")
# except sqlite3.OperationalError:
#     pass

with open("usercontent/settings.json") as file:
    setting = json.load(file)


class Money(commands.Cog, name="Money", description="Money and stuff"):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
        self.config = bot.config
        self.settings = setting

    @commands.command(name="money_start", brief="Adds you to the Money database")
    async def money_start(self, ctx):
        user = db.profiles.find_one(
            {
                "_id": ctx.author.id,
            }
        )

        if user:
            raise self.bot.errors.ProfileAlreadyExists(ctx.author.name)
        db.profiles.insert_one(
            {
                "_id": ctx.author.id,
                "name": ctx.author.name,
                "level": 1,
                "xp": 1,
                "wallet": 500,
                "bank": 0,
                "percentage": 100,
                "inventory": {"0": 2},
                "deaths": 0
            }
        )
        prof = db.profiles.find_one({"_id": ctx.author.id})
        print(prof["inventory"])

        await ctx.send("You have entered the Money experience! Have fun!")

    @commands.command(name="profile", brief="View your profile")
    async def profile(self, ctx):
        data = db.profiles.find_one({"_id": ctx.author.id})
        if not data:
            raise self.bot.errors.ProfileNotFound(ctx.author.name)
        items = data["inventory"]
        item_count = 0
        for _id, count in items.items():
            item_count += count
        embed = discord.Embed(
            title=f"{ctx.author.name}'s profile",
            color=ctx.author.color
        )
        embed.set_thumbnail(url=ctx.author.avatar.url)
        embed.add_field(name="Level", value=data["level"])
        embed.add_field(name="XP", value=data["xp"])
        embed.add_field(name="Money", value=f"Wallet: `{data['wallet']}$`\n"
                                            f"Bank: `{data['bank']}$`\n"
                                            f"Percentage: `{data['percentage']}%`")
        embed.add_field(name="Inventory",
                        value=f"`{item_count}` items")
        embed.add_field(name="Deaths", value=f"`{data['deaths']}`")
        await ctx.send(embed=embed)

    @commands.command(name="inventory", brief="Displays your inventory")
    async def inventory(self, ctx):
        embed = discord.Embed(
            title=f"{ctx.author.name}'s inventory",
            color=ctx.author.color
        )
        prof = db.profiles.find_one({"_id": ctx.author.id})
        if not prof:
            raise self.bot.errors.ProfileNotFound(ctx.author.name)

        inv = prof['inventory']
        for item, count in inv.items():
            if count == 0:
                break
            item = db.items.find_one({"_id": int(item)})
            embed.add_field(
                name=f"{item['emoji']} {item['name']} - {count}",
                value=f"**{item['desc']}**\nPrice: {item['trade_val']}$~{item['price']}$\n"
                      f"*ID `{item['_id']}`* - {item['type']}",
                inline=False
            )
        await ctx.send(embed=embed)

    @commands.command(name="item", brief="Searches for an item's stats")
    async def item(self, ctx, name):

        if name.isnumeric():
            item = db.items.find_one({"_id": int(name)})
        else:
            item = db.items.find_one({"name": name.lower()})

        embed = discord.Embed(
            title=f'{item["emoji"]} {item["name"].title()}',
            description=f"> {item['description']}\n"
                        f"**PRICE** - `{item['price']}$`\n"
                        f"**TRADE** - `{item['trade_val']}$`",
            color=discord.Color.random()
        )
        embed.add_field(name="Rarity", value=f"`{item['rarity']}`")
        embed.add_field(name="Type", value=f"`{item['type']}`")
        embed.add_field(name="ID", value=f'`{item["_id"]}`')
        embed.add_field(name="Part of", value=f"`{item['bundle']}` bundle", inline=False)

        await ctx.send(embed=embed)

    @commands.command(name="add_items", brief="Add new items from file")
    async def add_items(self, ctx):
        with open("usercontent/items.json") as f:
            items = json.load(f)
        for item in items:
            if not db.items.find_one({"_id": item["_id"]}):
                db.items.insert_one(item)


async def setup(bot):
    await bot.add_cog(Money(bot))
