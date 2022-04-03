import discord


def command_on_cooldown(seconds):
    embed = discord.Embed(
        title="That's too fast!",
        description=f"***{seconds}s** left of cooldown*",
        color=0xd89a52
    )
    return embed


def command_not_found():
    embed = discord.Embed(
        title="That command doesn't exist",
        description="Try another command",
        color=0xE3170A
    )
    return embed
