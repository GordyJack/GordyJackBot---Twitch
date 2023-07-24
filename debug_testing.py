import csv

import pyttsx3
from gtts import gTTS

import cogs.RedeemCog

# engine = pyttsx3.init()
#
# voices = engine.getProperty('voices')
# for voice in voices:
#     print("Voice:")
#     print(" - ID: %s" % voice.id)
#     print(" - Name: %s" % voice.name)
#     print(" - Languages: %s" % voice.languages)
#     print(" - Gender: %s" % voice.gender)
#     print(" - Age: %s" % voice.age)
#
# while True:
#     cogs.RedeemCog.tts(input('tts: '))

prisms = []
for a in range(2, 300 + 1, 2):  # Number of generators wide
    for b in range(1, 300 + 1):  # Number of Floors
        for c in range(1, 300 + 1):  # c Number of generators long
            if a * b * c == 300 and not (a > c):
                prisms.append((a, b, c))

prisms.sort(key=lambda x: (x[1], x[0]))

with open('logs/testing/prisms.csv', 'w', newline='') as csvfile:
    fieldnames = ['Index', 'Width', 'Height', 'Length', 'Surface', 'Width_Scaled', 'Height_Scaled', 'Length_Scaled',
                  'Surface_Scaled']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    for i, prism in enumerate(prisms):
        a = (prism[0], int(prism[0] * 3.5))
        b = (prism[1], prism[1] * 7)
        c = (prism[2], prism[2] * 3)
        surface = (a[0] * c[0], a[1] * c[1])

        # Write the data
        writer.writerow(
            {'Index': i + 1, 'Width': a[0], 'Height': b[0], 'Length': c[0], 'Surface': surface[0], 'Width_Scaled': a[1],
             'Height_Scaled': b[1], 'Length_Scaled': c[1], 'Surface_Scaled': surface[1]})
