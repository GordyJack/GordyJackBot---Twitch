import pyttsx3

import cogs.RedeemCog

engine = pyttsx3.init()

voices = engine.getProperty('voices')

for voice in voices:
    print("Voice:")
    print(f" - ID: {voice.id}")
    print(" - Name: %s" % voice.name)
    print(" - Languages: %s" % voice.languages)
    print(" - Gender: %s" % voice.gender)
    print(" - Age: %s" % voice.age)

while True:
    cogs.RedeemCog.tts(input('tts: '))
