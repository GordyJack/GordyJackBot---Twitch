import pyttsx3
from gtts import gTTS

import cogs.RedeemCog

while True:
    cogs.RedeemCog.google_text_to_speech(input('tts: '))
