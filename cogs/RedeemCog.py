import os
import random
import re

import pyttsx3

from dotenvy import load_env, read_file
from twitchio.ext import pubsub, commands

load_env(read_file('.env'))

users_oauth_token = os.getenv('CHANNEL_ACCESS_TOKEN')
users_channel_id = int(os.getenv('CHANNEL_ID'))


class RedeemCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.pubsub = pubsub.PubSubPool(bot)

    @commands.Cog.event()
    async def event_ready(self):
        print(f"{__name__} registered with | {self.bot.user_id}")
        print(f"RedeemCog channel ID | {users_channel_id}")
        topics = [
            pubsub.channel_points(users_oauth_token)[users_channel_id],
            pubsub.bits(users_oauth_token)[users_channel_id],
            pubsub.channel_subscriptions(users_oauth_token)[users_channel_id]
        ]
        await self.bot.pubsub.subscribe_topics(topics)

    @commands.Cog.event()
    async def event_pubsub_bits(self, event: pubsub.PubSubBitsMessage):
        bit_count = event.bits_used
        message = event.message
        user = event.user

        print(user, bit_count, message)

        pass  # do stuff on bit redemptions

    @commands.Cog.event()
    async def event_pubsub_channel_points(self, event: pubsub.PubSubChannelPointsMessage):
        reward = event.reward.title
        cost = event.reward.cost
        message = event.input
        status = event.status
        cooldown = event.reward.cooldown
        cooldown_until = event.reward.cooldown_until

        print(f"{reward} | {cost} | {message} | {status} | {cooldown} | {cooldown_until}")

        match reward:
            case "Hydrate!":
                print(reward)
            case "Timeout Somebody Else":
                print(reward, message)
            case "Ad Time":
                print("Run an Ad")
            case "Text to Speech":
                print(reward, message)
                tts(message)
        pass  # do stuff on channel point redemptions

    @commands.Cog.event()
    async def event_pubsub_subscription(self, event: pubsub.PubSubChannelSubscribe):
        print("SUBSCRIPTION", event.channel, event.user, event.message, event.time, event.multi_month_duration, event.cumulative_months, event.is_gift)


def tts(message):
    engine = pyttsx3.init()

    voice_ids = [voice.id for voice in engine.getProperty('voices')]
    voice_path = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\'
    default_voice = voice_path + 'TTS_MS_EN-US_DAVID_11.0'
    default_rate = 150
    default_volume = 1.0

    modifiers = {
        '{normal}': lambda: reset_to_default(),
        '{randomize}': None,
        '{male}': lambda: engine.setProperty('voice', default_voice),
        '{female}': lambda: engine.setProperty('voice', voice_path + 'TTS_MS_EN-US_ZIRA_11.0'),
        '{slow}': lambda: engine.setProperty('rate', default_rate*(2/3)),
        '{fast}': lambda: engine.setProperty('rate', default_rate*1.5),
        '{quiet}': lambda: engine.setProperty('volume', default_volume*(2/3)),
        '{loud}': lambda: engine.setProperty('volume', default_volume*1.5),
    }

    def randomize_properties():
        random_voice = random.choice(voice_ids)
        random_rate = random.randint(50, 200)
        random_volume = random.uniform(.5, 1.5)
        print(random_voice, random_rate, random_volume)
        engine.setProperty('voice', random_voice)
        engine.setProperty('rate', random_rate)
        engine.setProperty('volume', random_volume)

    def reset_to_default():
        engine.setProperty('voice', default_voice)
        engine.setProperty('rate', default_rate)
        engine.setProperty('volume', default_volume)

    parts = re.split('({.+?})', message)
    randomizing = False
    for part in parts:
        if part in modifiers:
            if part == '{randomize}':
                randomizing = True
            else:
                randomizing = False
                modifiers[part]()
        else:
            words = part.split()
            for word in words:
                if randomizing:
                    randomize_properties()
                engine.say(word)
        engine.runAndWait()


def prepare(bot):
    bot.add_cog(RedeemCog(bot))
