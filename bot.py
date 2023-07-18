# Imports
import atexit
import difflib
import os
import random

# Complex Imports
from datetime import datetime
from dotenvy import load_env, read_file
from twitchio.ext import commands
from twitchio.ext.commands import CommandNotFound

# Local Imports
import command_data_utils
import log_utils

load_env(read_file('.env'))

oauth_token = os.getenv('BOT_ACCESS_TOKEN')
channel_name = 'gordyjackstreaming'

cog_names = ['ChatCommandsCog', 'ModCommandsCog', 'RedeemCog', 'RoutineCog']


class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token=oauth_token, prefix='!', initial_channels=[channel_name])
        self.disabled_commands = {}

        self.first_chatter = ''
        self.last_chatter = ''
        self.last_chatters = []
        self.last_chatters_count = random.randint(5, 15)
        self.last_message = ''
        self.lurkers_list = []
        self.last_lurker = None
        self.reminder_count = 0
        self.message_count = 0

        self.log_messages = []

        self.command_data = command_data_utils.load_command_data()

        atexit.register(log_utils.save_chat_log, self.log_messages)

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

        for command, properties in self.command_data.items():
            print(command, properties)
            if command and properties and not properties["enabled"]:
                self.disabled_commands[command] = self.get_command(command)
                self.remove_command(command)

        for command in self.disabled_commands:
            try:
                self.remove_command(command)
            except CommandNotFound:
                continue

    async def event_message(self, message):
        self.log_messages.append(
            f"[{datetime.now().strftime(command_data_utils.get_date_format())}] {message.author.display_name if message.author is not None else 'GordyJackBot'}: {message.content}")

        self.last_message = message.content

        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            # await self.handle_commands(message)
            return

        author = message.author
        author_name = author.display_name
        self.last_chatter = author_name

        content = message.content
        self.message_count += 1

        # Print the contents of our message to console...
        print(self.message_count, author_name + ": " + content)

        # Do things based on message content
        if author in self.lurkers_list:
            self.lurkers_list.remove(author)
            print(self.lurkers_list)
        if self.message_count == 1:
            self.first_chatter = author_name
            await message.channel.send(f"Hello, {author_name}! You are the first chatter!")
        if self.message_count in (10, 100, 200, 500, 1000):
            await message.channel.send(f"Congrats, {author_name}! You sent the {self.message_count}th message!")
        if author_name in content:
            await message.channel.send(f"Congrats, {author_name}! You know your own name!")

        self.last_chatters.append(self.last_chatter)
        if len(self.last_chatters) == self.last_chatters_count and all(
                element == self.last_chatter for element in self.last_chatters):
            await message.channel.send(f"Dang, {author_name} you sure have been talking a lot. \
                {self.last_chatters_count} messages to be precise. I guess it must be lonely in here or something.")
            self.last_chatters_count = random.randint(5, 15)
            self.last_chatters.clear()

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    async def event_command_error(self, ctx, error: Exception) -> None:
        print(f'event_command_error: {ctx.message.content} | {error}')
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Command is on cooldown, please wait {error.retry_after:.0f} seconds.")
        elif isinstance(error, commands.CommandNotFound):
            attempted_command = ctx.message.content.split()[0][1:]

            if attempted_command in self.disabled_commands.keys():
                await ctx.send(f"The command: {attempted_command} is temporarily disabled")
                return

            closest_match = difflib.get_close_matches(attempted_command, self.commands.keys(), n=1)
            if closest_match:
                await ctx.send(f"{error} Did you mean '{closest_match[0]}'?")
            else:
                await ctx.send(str(error))
        else:
            await super().event_command_error(ctx, error)


if __name__ == "__main__":
    bot = Bot()
    for cog in cog_names:
        bot.load_module(f"cogs.{cog}")
    bot.run()
