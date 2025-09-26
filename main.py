from mido import MidiFile, MidiTrack, Message
import pandas as pd
import random

file = MidiFile()
track1 = MidiTrack()
track2 = MidiTrack()
file.tracks.append(track2)
file.tracks.append(track1)

melodies = pd.read_csv('melodies.csv',sep=";")
chords = pd.read_csv('chords.csv',sep=";")
#chordTimes = pd.read_csv('chordTimes.csv',sep=";")
#basicData = pd.read_csv("basicData.csv",sep";")

melody = melodies.iloc[:,0].tolist()
V = melodies.iloc[:,2].tolist()
#VII = melodies.iloc[:,3].tolist()
VIII = melodies.iloc[:,3].tolist()
melodyTimes = melodies.iloc[:,1].tolist()

bassType = pd.read_csv('bassType.csv',sep=";")
bassType = str(bassType.iloc[0,0])

#chordTimes = chordTimes.iloc[:,0].tolist()
#basicData = basicData.iloc[0,:].tolist()

#Acordes = chords.iloc[:,0:2]
#valoresTempos = chords.iloc[:,3].tolist()

bass = [random.randint(0, 2) for i in range(8)]

def writeChord(chord):
  
  for i in range(len(bass)):
    track1.append(Message('note_on', channel=0, note=int(chord[bass[i]]-12), velocity=64, time=0))
    track1.append(Message('note_off', channel=0, note=int(chord[bass[i]]-12), velocity=64, time=240))


def writeChord2(chord):
    track1.append(Message('note_on', channel=0, note=int(chord[0]), velocity=64, time=0))
    
    track1.append(Message('note_on', channel=0, note=int(chord[1]), velocity=64, time=0))
    track1.append(Message('note_on', channel=0, note=int(chord[2]), velocity=64, time=0))
    track1.append(Message('note_off', channel=0, note=int(chord[0]), velocity=64, time=240*8))
    track1.append(Message('note_off', channel=0, note=int(chord[1]), velocity=64, time=0))
    track1.append(Message('note_off', channel=0, note=int(chord[2]), velocity=64, time=0))
        
def writeNote(note,time,V,VIII):
  track2.append(Message('note_on', channel=0, note=int(note), velocity=64, time=0))
  
  if V != 0:
    track2.append(Message('note_on', channel=0, note=int(V), velocity=64, time=0))
  #if VII != 0:
  #  track2.append(Message('note_on', channel=0, note=int(VII), velocity=64, time=0))
  if VIII != 0:
    track2.append(Message('note_on', channel=0, note=int(VIII), velocity=64, time=0))
  
  track2.append(Message('note_off', channel=0, note=int(note), velocity=64, time=int(time)))

  if V != 0:
    track2.append(Message('note_off', channel=0, note=int(V), velocity=64, time=0))
  #if VII != 0:
  #  track2.append(Message('note_off', channel=0, note=int(VII), velocity=64, time=0))
  if VIII != 0:
    track2.append(Message('note_off', channel=0, note=int(VIII), velocity=64, time=0))

for n in range(len(melodyTimes)):
  writeNote(melody[n],melodyTimes[n],V[n],VIII[n])

if bassType == "Simple":
  for n in range(len(chords)):
    writeChord2(chords.iloc[n].tolist())
elif bassType == "Random Repeated":
  for n in range(len(chords)):
    writeChord(chords.iloc[n].tolist())

file.save('Music.mid')

