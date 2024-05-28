from music21 import *

s = stream.Stream()

# Choose a different instrument, e.g., Flute
desired_instrument = instrument.Flute()

for i in [60, 62, 65]:
    n = note.Note(i)
    n.quarterLength = 2
    n.volume.velocity = 127
    s.append(n)

s.show('midi')