import asyncio
import random

from pynput.keyboard import Controller, Key
from twitchio.ext import commands


class MinecraftCommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.all_commands = {
            "kill": "Kills the player.",
        }
        self.kb = Controller()

    @commands.Cog.event()
    async def event_ready(self):
        print(f"{__name__} registered with | {self.bot.user_id}")

    @commands.command()
    @commands.cooldown(1, random.randint(1800, 3600))
    async def kill(self, ctx: commands.Context):
        await self.enter_command('kill')

    async def enter_command(self, command: str):
        self.kb.type('/')
        await asyncio.sleep(.1)
        self.kb.type(command)
        await self.press_and_release_enter()

    async def press_and_release_enter(self, key=Key.enter):
        self.kb.press(key)
        self.kb.release(key)


def prepare(bot):
    bot.add_cog(MinecraftCommandsCog(bot))
