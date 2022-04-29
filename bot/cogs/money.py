import sqlite3


import discord
from discord.ext import commands


database = sqlite3.Connection("usercontent/money.db")
database.row_factory = sqlite3.Row
c = database.cursor()
try:
    c.execute("""CREATE TABLE profiles (
                 id INT, name TEXT, level INT, xp INT, wallet INT, bank INT, percentage INT, inventory BLOB, deaths INT
                 );""")
except sqlite3.OperationalError:
    pass
try:
    c.execute("""CREATE TABLE "items" (
                 id INT UNIQUE, emoji TEXT, name TEXT, desc TEXT, description TEXT, price INT, trade_val INT,
                 type TEXT, rarity TEXT, bundle TEXT,
                 PRIMARY KEY("id")
             );""")
    c.execute("INSERT INTO items VALUES (0, ':black_large_square:', 'nothing', 'it\'s nothing', 'it\'s nothing',"
              "0, 0, 'None', 'common', 'starters')")
except sqlite3.OperationalError:
    pass


class Money(commands.Cog, name="Money", description="Money and stuff"):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
        self.config = bot.config
        self.settings = bot.settings

    @commands.command(name="money_start", brief="Adds you to the Money database")
    async def money_start(self, ctx):
        with database:
            c.execute(f"SELECT * FROM profiles WHERE id={ctx.author.id}")
            if c.fetchone():
                raise self.bot.errors.ProfileAlreadyExists(ctx.author.name)
            c.execute("INSERT INTO profiles VALUES (:id, :name, 1, 1, 500, 0, 100, :inv, 0)",
                      {"id": ctx.author.id, "name": ctx.author.name, "inv": '0,0'})
            c.execute(f"SELECT * FROM profiles")
            print(c.fetchone()["inventory"])

        await ctx.send("You have entered the Money experience! Have fun!")

    @commands.command(name="profile", brief="View your profile")
    async def profile(self, ctx):
        with database:
            c.execute(f"SELECT * FROM profiles WHERE id={ctx.author.id}")
            data = c.fetchone()
            if not data:
                raise self.bot.errors.ProfileNotFound(ctx.author.name)
        embed = discord.Embed(
            title=f"{ctx.author.name}'s profile",
            color=ctx.author.color
        )
        embed.set_thumbnail(url=str(ctx.author.avatar_url))
        embed.add_field(name="Level", value=data["level"])
        embed.add_field(name="XP", value=data["xp"])
        embed.add_field(name="Money", value=f"Wallet: `{data['wallet']}$`\n"
                                            f"Bank: `{data['bank']}$`\n"
                                            f"Percentage: `{data['percentage']}%`")
        embed.add_field(name="Inventory",
                        value=f"`{len(data['inventory'].split(','))}` items")
        embed.add_field(name="Deaths", value=f"`{data['deaths']}`")
        await ctx.send(embed=embed)

    @commands.command(name="inventory", brief="Displays your inventory")
    async def inventory(self, ctx):
        embed = discord.Embed(
            title=f"{ctx.author.name}'s inventory",
            color=ctx.author.color
        )
        with database:
            c.execute(f"SELECT * FROM profiles WHERE id={ctx.author.id}")
            profile = c.fetchone()
            if not profile:
                raise self.bot.errors.ProfileNotFound(ctx.author.name)

            items = {}
            inv = profile['inventory'].split(',')
            for item in set(inv):
                count = ''.join(inv).count(item)
                c.execute(f"SELECT * FROM items WHERE id={str(item)}")
                item = c.fetchone()
                embed.add_field(name=f"{item['emoji']} {item['name']} - {count}",
                                value=f"**{item['desc']}**\nPrice: {item['trade_val']}$~{item['price']}$\n"
                                      f"*ID `{item['id']}`* - {item['type']}",
                                inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="item", brief="Searches for an item's stats")
    async def item(self, ctx, name):
        with database:
            if name.isnumeric():
                c.execute(f"SELECT * FROM items WHERE id='{name}'")
                item = c.fetchone()
            else:
                c.execute(f"SELECT * FROM items WHERE name='{name.lower()}'")
                item = c.fetchone()

        embed = discord.Embed(
            title=f'{item["emoji"]}{item["name"].title()}',
            description=f"> {item['description']}\n"
                        f"**PRICE** - `{item['price']}$`\n"
                        f"**TRADE** - `{item['trade_val']}$`",
            color=discord.Color.random()
        )
        embed.add_field(name="Rarity", value=f"`{item['rarity']}`")
        embed.add_field(name="Type", value=f"`{item['type']}`")
        embed.add_field(name="ID", value=f'`{item["id"]}`')
        embed.add_field(name="Part of", value=f"`{item['bundle']}` bundle", inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Money(bot))
