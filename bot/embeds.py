"""
kwanCore, a discord.py bot foundation.
Copyright (C) 2022  dopebnan

You should have received a copy of the GNU General Public License
along with kwanCore. If not, see <https://www.gnu.org/licenses/>.
"""

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
