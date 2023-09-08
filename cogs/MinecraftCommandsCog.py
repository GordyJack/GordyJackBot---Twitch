import asyncio
import random
import socket

from pynput.keyboard import Controller, Key
from twitchio.ext import commands

name_latch = True


def send_minecraft_command(command: str):
    global name_latch
    if name_latch:
        name_latch = False
        send_minecraft_command('set_player xkelley0529')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 8000)
    sock.connect(server_address)
    try:
        print(f'Sending {command}')
        sock.send(command.encode())
    finally:
        print('Closing Socket')
        sock.close()


class MinecraftCommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.all_commands = {
            'kill': 'Kills the player.',
        }
        self.kb = Controller()
        self.modpack = 'CHANGEME'

    @commands.Cog.event()
    async def event_ready(self):
        print(f'{__name__} registered with | {self.bot.user_id}')

    @commands.command()
    @commands.cooldown(1, random.randint(1800, 3600))
    async def kill(self, ctx: commands.Context):
        send_minecraft_command('kill')
        self.bot.remove_command('kill')

    @commands.command()
    @commands.cooldown(1, 300)
    async def modpack(self, ctx: commands.Context):
        await ctx.send(f'The modpack featured today is {self.modpack}')


def prepare(bot):
    bot.add_cog(MinecraftCommandsCog(bot))
