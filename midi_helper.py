from midiutil import MIDIFile
import mtheory as mt
import pygame
# import time
# import os
# import base64


def play_music(filename):
    pygame.init()
    clock = pygame.time.Clock()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        # check if playback has finished
        clock.tick(30)

def create_music(filename, midi_notes):
    """Creates a midi file with the nodes."""
    track    = 0
    channel  = 0
    time     = 1    # In beats
    duration = 3    # In beats          # let the sounds ring for more than their beat value
    tempo    = 400  # In BPM
    volume   = 100  # 0-127, as per the MIDI standard

    MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created automatically)
    MyMIDI.addTempo(track, time, tempo)
    for i, pitch in enumerate(midi_notes):
        if i == len(midi_notes) - 1: # if this is the last note, let it ring
            MyMIDI.addNote(track, channel, pitch, time + i, duration * 2, volume)
        else:
            MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)

    #program = 42 # A Cello
    #MyMIDI.addProgramChange(track, channel, time, program)

    if filename[-4:] != '.mid':
        filename = filename + '.mid'

    with open(filename, "wb") as output_file:
        MyMIDI.writeFile(output_file)


def create_music_chords(filename, chords):
    """Creates a midi file with the chords.
    Note: Expecting a list of chords with chord shapes like: ['D', 'C# min7b5']
    """
    track    = 0
    channel  = 0
    time     = 1    # In beats
    duration = 1    # In beats          # let the sounds ring for more than their beat value
    tempo    = 100  # In BPM
    volume   = 100  # 0-127, as per the MIDI standard

    MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created automatically)
    MyMIDI.addTempo(track, time, tempo)

    for i, chord in enumerate(chords):
        inversion = 0
        chord_details = chord.split(' ')
        chord_name = chord_details[0]
        if len(chord_details) > 1:
            chord_shape = chord_details[1]
            if len(chord_details) == 3:
                inversion = int(chord_details[2].replace('inv', ''))
        else:
            chord_shape = 'major'

        chord_notes = mt._get_chord('major', chord_name, inversion, chord_shape)
        #def get_chord(scale='major', base_note= 'C1', inversion=0, shape = 'basic', add_bass = False, base_degree = 1)

        for note in chord_notes:
            if i == len(chords) - 1: #if this is the last note, let it ring
                MyMIDI.addNote(track, channel, note, time + i, duration + 1, volume)
            else:
                MyMIDI.addNote(track, channel, note, time + i, duration, volume)

    #program = 42 # A Cello
    #MyMIDI.addProgramChange(track, channel, time, program)

    with open(filename, "wb") as output_file:
        MyMIDI.writeFile(output_file)
