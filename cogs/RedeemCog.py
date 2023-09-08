import librosa
import os
import random
import re
import soundfile as sf

import pyttsx3

from dotenvy import load_env, read_file
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
from twitchio.ext import pubsub, commands

from cogs import MinecraftCommandsCog

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
        message = event.message.content
        user = event.user

        print(user, bit_count, message)
        if bit_count >= 100:
            await tts(f"{'{randomize}'}{user} Cheered for {bit_count} bits: {message}")

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
                await tts("{randomize} HYDRATE!!!")
            case "Timeout Somebody Else":
                print(reward, message)
            case "Ad Time":
                print("Run an Ad")
            case "Text to Speech":
                print(reward, message)
                await tts(message)
            case "Have a Fruit!":
                print(reward)
                MinecraftCommandsCog.send_minecraft_command('chorus')

    @commands.Cog.event()
    async def event_pubsub_subscription(self, event: pubsub.PubSubChannelSubscribe):
        print("SUBSCRIPTION", event.channel, event.user, event.message, event.time, event.multi_month_duration,
              event.cumulative_months, event.is_gift)


async def tts(message):
    def randomize_properties():
        random_voice = random.choice(voice_ids)
        random_rate = random.randint(50, 200)
        random_volume = random.uniform(.01, 1.0)
        print(random_voice, random_rate, random_volume)
        engine.setProperty('voice', random_voice)
        engine.setProperty('rate', random_rate)
        engine.setProperty('volume', random_volume)

    def reset_to_default():
        # engine.setProperty('voice', default_voice)
        engine.setProperty('rate', default_rate)
        engine.setProperty('volume', default_volume)
    engine = pyttsx3.init()

    voice_ids = [voice.id for voice in engine.getProperty('voices')]
    voice_path = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\'
    default_voice = voice_path + 'TTS_MS_EN-US_DAVID_11.0'
    default_rate = 150
    default_volume = 0.5

    reset_to_default()

    modifiers = {
        '{normal}': lambda: reset_to_default(),
        '{randomize}': lambda: randomize_properties(),
        '{male}': lambda: engine.setProperty('voice', default_voice),
        '{female}': lambda: engine.setProperty('voice', voice_path + 'TTS_MS_EN-US_ZIRA_11.0'),
        '{slow}': lambda: engine.setProperty('rate', default_rate * (3 / 4)),
        '{fast}': lambda: engine.setProperty('rate', default_rate * 1.5),
        '{quiet}': lambda: engine.setProperty('volume', default_volume * (2 / 3)),
        '{loud}': lambda: engine.setProperty('volume', 1),
    }

    parts = re.split('({.+?})', message)
    for part in parts:
        if part in modifiers:
            modifiers[part]()
        else:
            engine.say(part)
        engine.runAndWait()


def google_text_to_speech(message: str):
    def create_audio_segment(text, tld, playback_speed=1.0, pitchshift=None):
        # Use gTTS to convert the text to speech
        speech = gTTS(text, lang='en', tld=tld)
        temp_filename = 'audio/temp.mp3'
        speech.save(temp_filename)

        if pitchshift is not None:
            pitch_shift(temp_filename, temp_filename, pitchshift)

        audio = AudioSegment.from_mp3(temp_filename)
        if playback_speed != 1.0:
            audio = audio.speedup(playback_speed=playback_speed)

        os.remove(temp_filename)

        return audio

    def pitch_shift(input_filename, output_filename, n_steps):
        # Load audio file
        y, sr = librosa.load(input_filename)

        # Shift pitch
        y_shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=n_steps)

        # Write out audio with shifted pitch
        sf.write(output_filename, y_shifted, int(sr))

    message = message.lower()

    modifiers = {
        'lang': {
            '{au}': 'com.au',  # For Male voice, we'll use UK English
            '{uk}': 'co.uk',  # For Female voice, we'll use US English
            '{us}': 'us',  # For Female voice, we'll use US English
            '{ca}': 'ca',  # For Female voice, we'll use US English
            '{in}': 'co.in',  # For Female voice, we'll use US English
            '{ie}': 'ie',  # For Female voice, we'll use US English
            '{za}': 'co.za'  # For Female voice, we'll use US English
        },
        '{slow}': 0.75,  # Slow down the audio speed by 75%
        '{fast}': 1.25,  # Speed up the audio by 125%
        '{low}': -10,  # Lower the pitch by 10 semitones
        '{normal}': None,  # Reset to default settings
        '{randomize}': 'random'  # Randomize settings
    }
    # Split the text into parts based on the modifiers
    parts = re.split('({.+?})', message)

    final_audio = AudioSegment.empty()
    accent = modifiers['lang']['{us}']
    speed = 1.0
    pitch = 0.0

    for part in parts:
        print(part)
        if part in modifiers['lang']:
            accent = modifiers['lang'][part]
        elif part in modifiers:
            match part:
                case '{randomize}':
                    lang = random.choice(modifiers['lang'].values())
                    speed = random.choice([0.75, 1.0, 1.25])
                    pitch = random.choice(range(-10, 10))
                case '{normal}':
                    lang = 'en'
                    speed = 1.0
                    pitch = 0.0
                case '{slow}' | '{fast}':
                    speed = modifiers[part]
                case '{low}':
                    pitch = modifiers[part]
        else:
            # Otherwise, create an audio segment with the current settings
            audio_segment = create_audio_segment(part, tld=accent, playback_speed=speed, pitchshift=pitch)
            final_audio += audio_segment

    # Save the final audio
    filename = "audio/final_audio.mp3"
    final_audio.export(filename, format="mp3")
    play(AudioSegment.from_mp3(filename))


def prepare(bot):
    bot.add_cog(RedeemCog(bot))
