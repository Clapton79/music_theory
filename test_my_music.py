import mtheory as mt
import midi_helper as mh
import os

#os.chdir ('C:\\Users\\leven\\Documents\\python\\music theory\\sound_files')

#autumn_leaves = ['F# min7b5 inv2', 'B m7', 'E m7', 'E m7 inv2', 'A m7', 'D 7', 'G maj7', 'C maj7']
#my_chord = mt.get_chord_info('F# min7b5 inv1')
#mh.play_music('output.mid')

#mh.create_music(input_file, autumn_leaves)
#mh.create_music_chords(input_file, practice)
#mh.play_music(input_file)

#scale = mt.explore_scale('major', 'C4', False)
#print (scale)

input_file = f"{os.getcwd()}\FSharp4ChordExploration.mid"
chord_family = 'harmonic minor'
base_note = 'F#4'
midi_notes = mt.explore_scale(chord_family, base_note, True, 1, True)

mh.create_music(input_file, midi_notes)
mh.play_music(input_file)
