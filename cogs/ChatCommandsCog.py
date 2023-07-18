import difflib
import random
from datetime import datetime

# import win32com
from twitchio.ext import commands

import command_data_utils
import log_utils


class ChatCommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_game = 'Satisfactory'
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
        await ctx.send("All commands: ")
        for command, description in self.all_commands.items():
            await ctx.send(f" --- {command} --- {description}")

    @commands.command(name='call_out_lurker')
    @commands.cooldown(1, 300, commands.Bucket.user)
    async def lurker_call_out(self, ctx: commands.Context):
        lurker = random.choice(self.bot.lurkers_list)
        await ctx.send(f"Hey! You! @{lurker.display_name}, Say Something!")

    # @commands.command()
    # @commands.cooldown(1, 90)
    # async def current_song(self, ctx: commands.Context):
    #     itunes = win32com.client.Dispatch("iTunes.Application")
    #     current_track = itunes.CurrentTrack
    #
    #     if current_track:
    #         artist = current_track.Artist
    #         title = current_track.Name
    #         await ctx.send(f"Now Playing: {title} by {artist}")
    #     else:
    #         await ctx.send("No song is playing.")

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
    @commands.cooldown(5, 60)
    async def get_colors(self, ctx: commands.Context, item_name: str = None):
        color_dict = {
            "Iron Ore": ("663633", "656f8c"),
            "Copper Ore": ("9d5a47", "405a61"),
            "Caterium Ore": ("e9d2a0", "a27a40"),
            "Limestone": ("c6b5ab", "89765f"),
            "Coal": ("050807", "0b0f15"),
            "Sulfur": ("ded267", "876421"),
            "Raw Quartz": ("ed82bc", "9d2a68"),
            "Bauxite": ("d29a80", "9c5548"),
            "Uranium Ore": ("448a3a", "173717"),
            "Leaves": ("4d6f43", "142c12"),
            "Wood": ("735e43", "2a1e14"),
            "Biomass": ("6b5f35", "3e3118"),
            "Solid Biofuel": ("847161", "3c2f25"),
            "Mycelia": ("8b8186", "3e3c49"),
            "Flower Petals": ("a94066", "7d8398"),
            "Fabric": ("978a85", "000003"),
            "Concrete": ("83755f", "c7c3c8"),
            "Iron Ingot": ("8e9298", "484948"),
            "Iron Plate": ("afb2b6", "4c4f54"),
            "Iron Rod": ("595b63", "1c1a22"),
            "Screw": ("99a2aa", "1164ce"),
            "Reinforced Iron Plate": ("9aa2b5", "59657e"),
            "Modular Frame": ("838baa", "5d5d5d"),
            "Copper Ingot": ("b07e7c", "553329"),
            "Copper Sheet": ("9e6d63", "325a8d"),
            "Wire": ("ab6c47", "846b4f"),
            "Cable": ("282a32", "6b6862"),
            "Copper Powder": ("7d5664", "afa4b6"),
            "Stator": ("444351", "59352c"),
            "Motor": ("47526f", "bf971f"),
            "Heavy Modular Frame": ("818896", "1b1b1b"),
            "Smart Plating": ("464b73", "a34033"),
            "Automated Wiring": ("26292e", "a34033"),
            "Caterium Ingot": ("cdba89", "927844"),
            "Quickwire": ("cdba89", "2a2e3f"),
            "Rotor": ("364364", "744029"),
            "Quartz Crystal": ("cb86c9", "3150b4"),
            "Silica": ("d3d4dd", "b2cedf"),
            "Crystal Oscillator": ("f7cf4e", "999198"),
            "Circuit Board": ("2b5533", "ffb85f"),
            "High-Speed Connector": ("2b5533", "415355"),
            "Steel Ingot": ("23272c", "0f1011"),
            "Steel Beam": ("292a2e", "703d30"),
            "Steel Pipe": ("323232", "703d30"),
            "Encased Industrial Beams": ("b3a891", "863f40"),
            "Versatile Framework": ("292a2d", "8b2819"),
            "Computer": ("c08e5a", "2e3531"),
            "Modular Engine": ("45444b", "a34033"),
            "Adaptive Control Unit": ("6b686c", "dfa05a"),
            "Assembly Director System": ("303032", "a34033"),
            "Magnetic Field Generator": ("303032", "9ad7b1"),
            "Nuclear Pasta": ("c08e5a", "93f8f7"),
            "Thermal Propulsion Rocket": ("303032", "a34033"),
            "Water": ("1f7ca1", "0d0d0e"),
            "Packaged Water": ("66a5c6", "0251b8"),
            "Crude Oil": ("111112", "0d0d0e"),
            "Packaged Crude Oil": ("0d0d0e", "d5d4d2"),
            "Heavy Oil Residue": ("85019a", "0d0d0e"),
            "Packaged Heavy Oil Residue": ("85019a", "d5d4d2"),
            "Fuel": ("cd812b", "0d0d0e"),
            "Packaged Fuel": ("f9a320", "10100e"),
            "Liquid Biofuel": ("263e1a", "0d0d0e"),
            "Packaged Liquid Biofuel": ("195200", "10100e"),
            "Turbofuel": ("810006", "0d0d0e"),
            "Packaged Turbofuel": ("d60710", "10100e"),
            "Empty Canister": ("64606a", "10100e"),
            "Alumina Solution": ("b4b1b7", "0d0d0e"),
            "Packaged Alumina Solution": ("bdc0cc", "dcaf4c"),
            "Sulfuric Acid": ("d1c83a", "0d0d0e"),
            "Packaged Sulfuric Acid": ("b2ae4f", "42434f"),
            "Nitric Acid": ("d8d8bc", "0d0d0e"),
            "Nitrogen Gas": ("b0acb4", "0d0d0e"),
            "Packaged Nitrogen Gas": ("23273b", "b7b9c6"),
            "Packaged Nitric Acid": ("cfcfdb", "454550"),
            "Plastic": ("4dacf2", "221f24"),
            "Polymer Resin": ("252fd4", "060330"),
            "Rubber": ("1e1d1d", "cfb65e"),
            "Petroleum Coke": ("2b2c34", "060602"),
            "Empty Fluid Tank": ("7b95bd", "99969b"),
            "Compacted Coal": ("171a24", "0d0c09"),
            "Black Powder": ("1c1d23", "c8000a"),
            "Smokeless Powder": ("0c0c0c", "df1720"),
            "AI Limiter": ("1c1c1a", "648d8c"),
            "Supercomputer": ("222327", "f1bf74"),
            "Radio Control Unit": ("2b2b2b", "e2bc26"),
            "Heat Sink": ("949796", "a1663e"),
            "Battery": ("2d3146", "adadbc"),
            "Fused Modular Frame": ("a5a5a6", "f4aa53"),
            "Cooling System": ("de9860", "999da1"),
            "Turbo Motor": ("2c3034", "cfa011"),
            "Quantum Computer": ("1f1f1f", "e6b16d"),
            "Pressure Conversion Cube": ("d49058", "1f2133"),
            "Superposition Oscillator": ("adaea0", "edc888"),
            "Aluminum Scrap": ("abaaae", "c6841c"),
            "Aluminum Ingot": ("b9bcc3", "666a6c"),
            "Alclad Aluminum Sheet": ("afb2bc", "818073"),
            "Aluminum Casing": ("aaa9ae", "1f2228"),
            "Encased Uranium Cell": ("d8d11b", "8beac3"),
            "Non-fissile Uranium": ("e7e334", "8beac3"),
            "Uranium Fuel Rod": ("1e1e15", "64c987"),
            "Nuclear Waste": ("d9d423", "1cb83b"),
            "Plutonium Pellet": ("758b8f", "72bacd"),
            "Encased Plutonium Cell": ("2b3230", "a8e5e9"),
            "Plutonium Fuel Rod": ("cebe40", "a8e5e9"),
            "Plutonium Waste": ("b6ac23", "71cae3"),
            "Electromagnetic Control Rod": ("383941", "ede954"),
            "Beryl Nut": ("bba775", "b8cace"),
            "Pale Berry": ("f27954", "b14244"),
            "Bacon Agaric": ("f2e2e2", "d7577c"),
            "Medicinal Inhaler": ("ededec", "47aee1"),
            "Hog Remains": ("a38da8", "554051"),
            "Spitter Remains": ("6c5982", "972e37"),
            "Hatcher Remains": ("454792", "e394ae"),
            "Stinger Remains": ("1a1c20", "a07277"),
            "Alien Protein": ("654368", "c9cbce"),
            "Alien DNA Capsule": ("96949d", "2e3531"),
            "Hard Drive": ("994f29", "313130"),
            "Ficsit Coupon": ("e49246", "e9a86a"),
            "Blade Runners": ("092e57", "050505"),
            "Hazmat Suit": ("d2b763", "424462"),
            "Jetpack": ("ffb85c", "373938"),
            "Hover Pack": ("ffb85c", "373938"),
            "Gas Mask": ("eda048", "242122"),
            "Gas Filter": ("8e859c", "131211"),
            "Iodine Infused Filter": ("b6881f", "121311"),
            "Build Gun": ("d99427", "24282b"),
            "Color Gun": ("e38f3f", "1c1b1d"),
            "Object Scanner": ("cd7f24", "151517"),
            "Xeno-Zapper": ("e38f32", "383f52"),
            "Xeno-Basher": ("e2872f", "51c1c8"),
            "Rebar Gun": ("2c2d30", "0d0d0e"),
            "Iron Rebar": ("d27e13", "222025"),
            "Shatter Rebar": ("772e6e", "222025"),
            "Stun Rebar": ("017bb2", "222025"),
            "Explosive Rebar": ("a50810", "222025"),
            "Nobelisk Detonator": ("dcc109", "aa0003"),
            "Nobelisk": ("a00509", "f7f420"),
            "Gas Nobelisk": ("5b7a29", "fcda40"),
            "Pulse Nobelisk": ("8eaab6", "fcda40"),
            "Cluster Nobelisk": ("f39f26", "fb6f58"),
            "Nuke Nobelisk": ("424d49", "72c48a"),
            "Rifle": ("faca42", "272728"),
            "Rifle Ammo": ("cc6927", "050504"),
            "Smart Rifle Ammo": ("272a2d", "423a1b"),
            "Turbo Rifle Ammo": ("c12b31", "090807"),
            "Boombox": ("d6953c", "1f2122"),
            "Chainsaw": ("dd832c", "1d202b"),
            "Zipline": ("d48020", "c8b684"),
            "FICSMAS Gift": ("f0c07a", "d92020"),
            "Red FICSMAS Ornament": ("db0108", "7f0000"),
            "Copper FICSMAS Ornament": ("fea318", "844e01"),
            "Iron FICSMAS Ornament": ("ffffff", "9f9b98"),
            "Blue FICSMAS Ornament": ("1dc0e7", "004f78"),
            "Candy Cane": ("ad0000", "ecdccc"),
            "FICSMAS Wonder Star": ("f9dd2c", "d79103"),
            "FICSMAS Bow": ("f13f2c", "c6080c"),
            "FICSMAS Decoration": ("404124", "c6080c"),
            "Actual Snow": ("fde9d0", "cbc4e0"),
            "Snowball": ("f9ebf7", "dcd6e1"),
            "Snowball Pile": ("f9eaf9", "e3cbbb"),
            "Snowman": ("fbebe2", "cf0c13"),
            "Giant FICSMAS Tree": ("322b12", "121607"),
            "FICSMAS Gift Tree": ("5d4b28", "910002"),
            "FICSMAS Wreath": ("704b15", "910002"),
            "FICSMAS Tree Branch": ("8487a3", "6e5b5b"),
            "Power Shard": ("c6712f", "86c0e9"),
            "Blue Power Slug": ("7bbfdd", "6b74ad"),
            "Yellow Power Slug": ("e7b55a", "e79763"),
            "Purple Power Slug": ("df88e5", "b250d0"),
            "SAM Ingot": ("124354", "2c0436"),
            "FICSIT Coffee Cup™": ("bb7c51", "3ea2d3"),
            "'Employee of the Planet' Cup": ("cda44e", "2a2930"),
            "Mercer Sphere": ("010101", "407246"),
            "Somersloop": ("5e0311", "440d39"),
            "Player": ("ccb692", "dd9a5a")
        }

        print(item_name)
        item_name = difflib.get_close_matches(item_name, color_dict.keys(), n=1)[
            0] if item_name not in color_dict.keys() else item_name

        if item_name is None:
            await ctx.send("get_color usage: !get_color [item_name] [0 or 1]")
        else:
            await ctx.send(
                f"The colors of {item_name} are: #{color_dict[item_name][0]} and #{color_dict[item_name][1]}")

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
            questions = get_game_questions(self.current_game)
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
        questions = get_game_questions(self.current_game)
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
