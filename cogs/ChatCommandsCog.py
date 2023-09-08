import difflib
import random
from datetime import datetime

import win32com
# import win32com
from twitchio.ext import commands

import command_data_utils
import log_utils


class ChatCommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.all_commands = {
            "50th": "Gives a shoutout and thank you to my 50th follower.",
            "commands": "Lists all commands.",
            "call_out_lurker": "Calls out a random lurker to invite them into the conversation.",
            "current_song": "Lets you know the current song that is playing.",
            "discord": "Provides the Discord server invitation link.",
            "easter_eggs": "Lists all Easter Eggs.",
            "get_colors": "Input a named item from Satisfactory to get its colors.",
            "first": "Announces who the first chatter of the stream was.",
            "lurk": "Sets you as a lurker.",
            "lurkers": "Lets you know the number of lurkers.",
            "qotd": "Asks the question of the day.",
            "rand_question": "Asks a random question.",
            "top_chatter": "Announces who the top chatter last stream was."
        }

    @commands.Cog.event()
    async def event_ready(self):
        print(f"{__name__} registered with | {self.bot.user_id}")

    async def global_before_invoke(self, ctx):
        command = ctx.message.split()[0][1:]
        if command in self.all_commands.keys():
            command_data_utils.update_last_used(command)

    @commands.command(name='commands')
    @commands.cooldown(1, 600)
    async def show_commands(self, ctx: commands.Context):
        await ctx.send("Check out the commands panel down below the stream!")
        # await ctx.send("All commands: ")
        # for command, description in self.all_commands.items():
        #     await ctx.send(f" --- {command} --- {description}")

    @commands.command(name='call_out_lurker')
    @commands.cooldown(1, 300, commands.Bucket.user)
    async def lurker_call_out(self, ctx: commands.Context):
        lurker = random.choice(self.bot.lurkers_list)
        await ctx.send(f"Hey! You! @{lurker.display_name}, Say Something!")

    @commands.command()
    @commands.cooldown(1, 90)
    async def current_song(self, ctx: commands.Context):
        itunes = win32com.client.Dispatch("iTunes.Application")
        current_track = itunes.CurrentTrack

        if current_track:
            artist = current_track.Artist
            title = current_track.Name
            await ctx.send(f"Now Playing: {title} by {artist}")
        else:
            await ctx.send("No song is playing.")

    @commands.command()
    @commands.cooldown(5, 300)
    async def discord(self, ctx: commands.Context):
        await ctx.send("https://discord.gg/YuWSRFbHMB")

    @commands.command(name="50th")
    @commands.cooldown(5, 600)
    async def fiftieth(self, ctx: commands.Context):
        await ctx.send("PelicanLeo was the 50th Follower! Thank you for affiliate PelicanLeo! And everyone else of "
                       "course...")

    @commands.command()
    @commands.cooldown(5, 600)
    async def first(self, ctx: commands.Context):
        await ctx.send(f"{self.bot.first_chatter} was the first chatter this stream!")

    @commands.command()
    async def lurk(self, ctx: commands.Context):
        self.bot.lurkers_list.append(ctx.author)
        print(self.bot.lurkers_list)

    @commands.command()
    @commands.cooldown(1, 600, commands.Bucket.user)
    async def lurkers(self, ctx: commands.Context):
        lurker_count = len(self.bot.lurkers_list)
        if lurker_count > 0:
            await ctx.send(f'There are {lurker_count} chatters lurking right now.')
        else:
            await ctx.send('There are no lurkers currently.')

    @commands.command()
    @commands.cooldown(1, 300, commands.Bucket.user)
    async def qotd(self, ctx: commands.Context):
        now = datetime.now()
        today = now.date()

        qotd_last_used = command_data_utils.get_command_property('qotd', 'last_used')
        then = datetime.strptime(qotd_last_used, command_data_utils.get_date_format()).date()

        last_qotd = command_data_utils.get_command_property('qotd', 'question')

        if today > then or last_qotd == '':
            questions = get_game_questions(self.bot.game)
            question = random.choice(questions)
            command_data_utils.save_command_property('qotd', 'question', question)
        elif last_qotd != '':
            question = last_qotd
        else:
            print('[ERROR]: qotd')
            return

        await ctx.send(question)

    @commands.command()
    @commands.cooldown(1, 150, commands.Bucket.user)
    async def rand_question(self, ctx: commands.Context):
        questions = get_game_questions(self.bot.game)
        question = random.choice(questions)
        await ctx.send(question)

    @commands.command()
    @commands.cooldown(2, 300)
    async def top_chatter(self, ctx: commands.Context):
        top_chatter = log_utils.get_top_chatter(log_utils.get_most_recent(), "GordyJackBot")
        if top_chatter:
            await ctx.send(f"The top chatter last stream was: {top_chatter}")
        else:
            await ctx.send(f"No chatters found in the latest log file.")


def get_game_questions(game):
    base_questions = [
        "What's your favorite food and why?",
        "If you could visit anywhere in the world, where would you go?",
        "What's the last book you read?",
        "What's your favorite movie or TV show?",
        "What hobbies do you enjoy in your free time?",
        "If you could have any superpower, what would it be?",
        "What's your favorite animal?",
        "What's your favorite video game?",
        "What's the most challenging video game you've ever played?",
        "Who is your favorite streamer and why?",
        "What is your favorite season of the year?",
        "If you could meet any historical figure, who would it be?",
        "What's your dream job?",
        "What's the first video game you ever played?",
        "What's your favorite genre of music?",
        "Do you prefer coffee or tea?",
        "What's your favorite board game?",
        "What's your favorite type of cuisine?",
        "What's your favorite video game character?",
        "What's your favorite thing about Twitch?",
        "What's your favorite sport?",
        "What's your favorite piece of technology that you own?",
        "What's your favorite holiday?",
        "What's the most memorable dream you've ever had?",
        "What's your favorite thing about the video game community?",
        "What's your favorite dessert?",
        "What's the best concert or live performance you've ever attended?",
        "What's your favorite quote?",
        "If you could live in any video game world, which one would you choose?",
        "What's something you've learned recently?"
    ]

    game_specific_questions = {
        "Satisfactory": [
            "What's the biggest factory you've built in Satisfactory?",
            "What's your favorite part of the Satisfactory map?",
            "What's the most challenging thing about playing Satisfactory?",
            "What's your strategy for resource management in Satisfactory?",
            "What's the coolest thing you've built in Satisfactory?",
            "What's your favorite biome in Satisfactory?",
            "What's your favorite vehicle in Satisfactory?",
            "What's the most difficult enemy you've faced in Satisfactory?",
            "What's your favorite resource to gather in Satisfactory?",
            "What's the longest conveyor belt you've built in Satisfactory?",
            "What's the most complex machine you've built in Satisfactory?",
            "What's your strategy for exploration in Satisfactory?",
            "What's the biggest challenge you've faced in Satisfactory?",
            "What's your favorite thing about the Satisfactory community?",
            "What tips would you give to a new Satisfactory player?"
        ],
        "Game2": [
            # Insert 15 questions specific to Game2 here...
        ],
        # Add more games as needed...
    }
    questions = base_questions.copy()
    if game in game_specific_questions:
        questions += game_specific_questions[game]
    return questions


def prepare(bot):
    bot.add_cog(ChatCommandsCog(bot))
