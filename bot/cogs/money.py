from pymongo import MongoClient
import json
import time

import discord
from discord.ext import commands, tasks

# TODO: start mongodb in the usercontent/db dir via mongod --dbpath ./
# TODO: mongosh: db.<collection name>.find()

dbcli = MongoClient()
db = dbcli.money


with open("usercontent/settings.json") as file:
    setting = json.load(file)


def effect_parse(effects: list[dict]) -> str:
    res = ""
    for effect in effects:
        res += f"**{effect['name']}** expires at <t:{int(effect['end'])}:t> (<t:{int(effect['end'])}:R>)\n"
    return res or "No active effects :D"


class Money(commands.Cog, name="Money", description="Money and stuff"):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
        self.config = bot.config
        self.settings = setting

    @tasks.loop(hours=1)
    async def money_check(self):
        # TODO: iterate through every user and check if they have any active effects
        # TODO: if not, then clear it
        # TODO: the effect's use will be checked at i.e., death, and then we don't need to worry about
        # TODO: weird time loopings to remove it at the right time, cuz it won't work where it doesn't need to

        self.logger.log("info", "money_check", f"finished the checks")

    @commands.command(name="money_start", brief="Adds you to the Money database")
    async def money_start(self, ctx):
        user = db.profiles.find_one({"_id": ctx.author.id, })

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
                "inventory": {"0": 2, "1": 1},
                "deaths": 0,
                "effects": []
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
        n = len(data["effects"])
        k = 0
        for i in range(n):
            if data["effects"][k]["end"] < time.time():
                data["effects"].pop(k)
            else:
                k = k + 1
        db.profiles.update_one({"_id": ctx.author.id},
                               {"$set": {'effects': data["effects"]}})
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
        # TODO: clean up the active effects thinga
        embed.add_field(name="Active Effects", value=effect_parse(data["effects"]))
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
                value=f"**{item['description']}**\nPrice: {item['trade_value']}$~{item['price']}$\n"
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

        await ctx.send("Addded new items")

    @commands.command(name="use", brief="use item from inventory")
    async def use_item(self, ctx, name):
        prof = db.profiles.find_one({"_id": ctx.author.id})
        if not prof:
            raise self.bot.errors.ProfileNotFound(ctx.author.name)

        if name.isnumeric():
            if name in prof["inventory"].keys() and prof["inventory"][name]:
                item = db.items.find_one({"_id": int(name)})
            else:
                raise self.bot.errors.ItemNotFound(name)
        else:
            item = db.items.find_one({"name": name.title()})
            if not str(item["_id"]) in list(prof["inventory"].keys()):
                raise self.bot.errors.ItemNotFound(name)

        n = len(item["effects"])
        for i in range(n):
            item["effects"][i]["start"] = time.time()
            item["effects"][i]["end"] = time.time() + item["effects"][i]["length"] * 60

        prof["effects"] += item["effects"]
        if prof["inventory"][str(item["_id"])] == 1:
            prof["inventory"].pop(str(item["_id"]), None)
        else:
            prof["inventory"][str(item["_id"])] -= 1
        db.profiles.update_one(
            {"_id": ctx.author.id},
            {
                "$set": {'effects': prof["effects"]},
                "$set": {'inventory': prof["inventory"]}
            }
        )

        # TODO: logging duh
        await ctx.send("Used item")


async def setup(bot):
    await bot.add_cog(Money(bot))
