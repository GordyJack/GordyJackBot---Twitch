import random
from twitchio.ext import routines, commands

channel_name = 'gordyjackstreaming'


class RoutineCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel = None
        self.last_message = bot.last_message if bot.last_message else None
        self.last_lurker = None

    @commands.Cog.event()
    async def event_ready(self):
        print(f"{__name__} registered with | {self.bot.user_id}")

        # Get properties from the bot here
        self.channel = self.bot.get_channel(channel_name)

        # Start all routines here
        self.call_out_lurker.start()
        self.follow_reminder.start()

    @routines.routine(seconds=random.randint(900, 1800))
    async def call_out_lurker(self):
        lurkers = self.bot.lurkers_list
        if self.channel and lurkers and ("feel free to join the chat!" not in self.last_message.content):  # if there are any lurkers
            lurker = random.choice(lurkers)  # selects a random lurker
            if lurker is not self.last_lurker:  # gets the specific channel
                await self.channel.send(f"Hey {lurker.display_name}, feel free to join the chat!")  # calls out the lurker
            else:
                print(f"[ERROR]: lurker_reminder_2 | {lurkers=} | {lurker=}")
        else:
            print(f"[ERROR]: lurker_reminder_1 | {lurkers=}")

    @routines.routine(seconds=random.randint(900, 1800))
    async def follow_reminder(self):
        last_message = self.bot.last_message
        reminder_message = "If you're liking the stream, don't forget to follow and join the !discord, " \
                           "so you can stay up to date on all my streams!"

        if self.channel and ((not last_message) or last_message != reminder_message):
            await self.channel.send(reminder_message)
        else:
            print("[ERROR]: follow_reminder")


def prepare(bot):
    bot.add_cog(RoutineCog(bot))
