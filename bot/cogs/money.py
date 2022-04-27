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


class Money(commands.Cog, name="Money", description="Money and stuff"):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
        self.config = bot.config
        self.settings = bot.settings

    @commands.command(name="money_start", brief="Add yourself to the Money experience")
    async def money_start(self, ctx):
        with database:
            c.execute(f"SELECT * FROM profiles WHERE id={ctx.author.id}")
            if c.fetchone():
                raise self.bot.errors.ProfileAlreadyExists(ctx.author.name)
            c.execute("INSERT INTO profiles VALUES (:id, :name, 1, 1, 500, 0, 100, :inv, 0)",
                      {"id": ctx.author.id, "name": ctx.author.name, "inv": ','})
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


def setup(bot):
    bot.add_cog(Money(bot))
