import disnake
import asyncio
from disnake import ButtonStyle
from disnake.ext import commands
from disnake.ui import View, Button
from datetime import datetime, timezone, timedelta


class MinecraftDonateSystem(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(MinecraftDonateSystem(bot))
