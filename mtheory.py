#import midiutil
import itertools
import collections
import regex as re

sound_sharps = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#','A', 'A#', 'B']
sound_flats  = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
MIDI_C_NOTE = 12

chord_families = {

                    'major'                 :{'scale': [2,2,1,2,2,2,1], 'degree': 1, 'family' : 'major'}
                ,   'dorian'                :{'scale': [2,1,2,2,2,1,2], 'degree': 2, 'family' : 'major'}
                ,   'phrygian'              :{'scale': [1,2,2,2,1,2,2], 'degree': 3, 'family' : 'major'}
                ,   'lidyan'                :{'scale': [2,2,2,1,2,2,1], 'degree': 4, 'family' : 'major'}
                ,   'mixolydian'            :{'scale': [2,2,1,2,2,1,2], 'degree': 5, 'family' : 'major'}
                ,   'natural minor'         :{'scale': [2,1,2,2,1,2,2], 'degree': 6, 'family' : 'major'}
                ,   'locrian'		        :{'scale': [1,2,2,1,2,2,2], 'degree': 7, 'family' : 'major'}

                ,   'melodic minor'         :{'scale': [2,1,2,2,1,2,2], 'degree': 1, 'family': 'melodic minor'}
                ,   'dorian b2'		        :{'scale': [1,2,2,1,2,2,2], 'degree': 2, 'family': 'melodic minor'}
                ,   'lydian augmented'	    :{'scale': [2,2,1,2,2,2,1], 'degree': 3, 'family': 'melodic minor'}
                ,   'lydian dominant'	    :{'scale': [2,1,2,2,2,1,2], 'degree': 4, 'family': 'melodic minor'}
                ,   'aeolian dominant'	    :{'scale': [1,2,2,2,1,2,2], 'degree': 5, 'family': 'melodic minor'}
                ,   'half diminished'	    :{'scale': [2,2,2,1,2,2,1], 'degree': 6, 'family': 'melodic minor'}
                ,   'altered'		        :{'scale': [2,2,1,2,2,1,2], 'degree': 7, 'family': 'melodic minor'}


                ,   'harmonic minor'		:{'scale': [2,1,2,2,1,3,1], 'degree': 1, 'family': 'harmonic minor'}
                ,   'locrian natural 6'		:{'scale': [1,2,2,1,3,1,2], 'degree': 2, 'family': 'harmonic minor'}
                ,   'major #5'		        :{'scale': [2,2,1,3,1,2,1], 'degree': 3, 'family': 'harmonic minor'}
                ,   'dorian #4'		    	:{'scale': [2,1,3,1,2,1,2], 'degree': 4, 'family': 'harmonic minor'}
                ,   'phrygian dominant'		:{'scale': [1,3,1,2,1,2,2], 'degree': 5, 'family': 'harmonic minor'}
                ,   'lydian #2'		    	:{'scale': [3,1,2,1,2,2,1], 'degree': 6, 'family': 'harmonic minor'}
                ,   'altered dominant bb7'	:{'scale': [1,2,1,2,2,1,3], 'degree': 7, 'family': 'harmonic minor'}

                ,   'harmonic major'		:{'scale': [2,2,1,2,1,3,1], 'degree': 1, 'family': 'harmonic major'}
                ,   'dorian b5'		    	:{'scale': [2,1,2,1,3,1,2], 'degree': 2, 'family': 'harmonic major'}
                ,   'phrygian b4'		    :{'scale': [1,2,1,3,1,2,2], 'degree': 3, 'family': 'harmonic major'}
                ,   'lydian b3'		    	:{'scale': [2,1,3,1,2,2,1], 'degree': 4, 'family': 'harmonic major'}
                ,   'mixolydian b2'			:{'scale': [1,3,1,2,2,1,2], 'degree': 5, 'family': 'harmonic major'}
                ,   'lydian augmented'		:{'scale': [3,1,2,2,1,2,1], 'degree': 6, 'family': 'harmonic major'}
                ,   'locrian bb7'	        :{'scale': [1,2,2,1,2,1,3], 'degree': 7, 'family': 'harmonic major'}

                ,	'diminished'		    :{'scale': [2,1,2,1,2,1,2], 'degree': 1, 'family': 'diminished'}
                ,	'inverted diminished'	:{'scale': [1,2,1,2,1,2,1], 'degree': 2, 'family': 'diminished'}

                ,	'whole tone'		    :{'scale': [2,2,2,2,2],     'degree': 1, 'family': 'whole tone'}

                ,	'augmented'		    	:{'scale': [3,1,3,1,3,1],   'degree': 1, 'family': 'augmented'}
                ,	'inverted augmented'	:{'scale': [1,3,1,3,1,3],   'degree': 2, 'family': 'augmented'}

}


chord_shapes = {
            'major'     :['1', '3', '5']
        ,   'maj7'      :['1', '3', '5','7']
        ,   'm7'        :['1', 'b3', '5','b7']
        ,   '7'         :['1', '3', '5','7']
        ,   'm7b5'      :['1', 'b3', 'b5','b7']
        ,   'm7#5'      :['1', 'b3', '#5','b7']
        ,   'm7#5b9'    :['1', 'b3', '#5','b7', 'b9']
        ,   'm7#5#9'    :['1', 'b3', '#5','b7', '#9']
        ,   'm7b5#9'    :['1', 'b3', 'b5','b7', '#9']
        ,   'm7b9'      :['1', '3', '5','b7', 'b9']
        ,   'm7b5b9'    :['1', 'b3', 'b5','b7', 'b9']
        ,   '7b5#9'     :['1', '3', 'b5','b7', '#9']
        ,   '7#9b13'    :['1', '3', 'b5','b7', '#9', 'b13']
        ,   'sus4'      :['1', '3', '4']
        ,   'maj7b5'    :['1', '3', 'b5','7']
        ,   'min'       :['1', 'b3', '5']
        ,   'minb5'     :['1', 'b3', 'b5']
        ,   'min7'      :['1', 'b3', '5','b7']
        ,   'min7b5'    :['1', 'b3', 'b5','b7']
        ,   'add9'      :['1', '3', '5', '9']
        ,   'add13'     :['1', '3', '5', '13']
        ,   'add9/11'   :['1', '3', '5', '11']
}


def get_scale(scale, base_note = 60, octaves = 1, close_with_base = False, reverse = False):
# returns a list for a scale

    try:
        degrees= [x['scale'] for i, x in  chord_families.items() if i == scale][0]
        #degrees = [0]+ degrees
        if octaves>1:
            result = []
            for o in range(octaves):
                result = result + get_scale(scale, base_note+(12*o), 1)

        else:
            result = [base_note + sum(degrees[:i]) for i,x in enumerate(degrees)]

        if close_with_base == True:
            result.append(base_note + (12*octaves))

        if reverse == True:
            result.reverse()

        return result
    except IndexError:
        return []


def get_number(my_string):
# keeps just the numbers in a text
    try:
        return int(re.sub('[^\-0-9]', '', my_string))
    except:
        return 4


def get_text(my_string):
# removes numbers from a text
    return (re.sub('[\-0-9]', '', my_string))


def find_note (note):
# finds the index of a note in the list of notes
    if note not in sound_sharps and note not in sound_flats:
        raise ValueError('Note does not exist')
    if note in sound_sharps:
        return sound_sharps.index(note)
    elif note in sound_flats:
        return sound_flats.index(note)


def get_note_id(note):
# searches for the midi note id

    i = find_note(get_text(note))
    note_level = get_number(note)

    note_id = MIDI_C_NOTE + i + note_level * 12
    return note_id


def get_chord_shape(shape):
# returns a list of what degrees and what alterations a chord has
    try:
    #(get_number(x)-1)
        alteration = []
        degrees = [get_number(x) for x in chord_shapes[shape]]
        alt = [get_text(x) for x in chord_shapes[shape]]
        for a in alt:
            if a == '':
                alteration.append(0)
            if a == 'b':
                alteration.append(-1)
            if a == '#':
                alteration.append(1)
        return degrees, alteration
    except IndexError:
        return [], []
    except KeyError:
        return [], []


def get_chord(scale='major', base_note= 'C1', inversion=0, shape = 'major', add_bass = False, bass_degree = 1):
# returns a list of chord sounds
    base_note_id = get_note_id(base_note)

    if inversion>3 or inversion<0:
        raise ValueError  ('Invalid inversion')
    scale_notes = get_scale(scale, base_note_id, 2)

    if len(scale_notes) == 0:
        return []
    else:
        degrees, alteration = get_chord_shape(shape)
        chord = [scale_notes[a-1] for a in degrees]
        chord = [a + alteration[i] for i, a in enumerate(chord)]

    if inversion == 1:
        chord[0] = chord[0]+12
    elif inversion ==2:
        chord[0] = chord[0]+12
        chord[1] = chord[1]+12

    if add_bass:
        bass_note_id=base_note_id-12    # bass note defaults to an octave lower
        if bass_degree == 1:
            bass_note_id = base_note_id -12
        else:
            bass_scale = get_scale(scale, bass_note_id)
            bass_note_id = bass_scale[bass_degree-1]
        chord.append(bass_note_id)

    return sorted(chord)


def get_list_note_ids(notes):
# returns up the midi note id's of a list of notes
    note_ids = []
    for note in notes:
        note_ids.append(get_note_id(note))
    return note_ids

def get_chord_info(chord):
# breaks down a chord into parts, then looks up its notes
    chord_details = chord.split(' ')
    #defaults
    shape = 'major'
    scale = 'major'
    inversion = 0
    base_note = chord_details[0]

    if len(chord_details) == 2:  # chord with alteration or inversion
        if 'inv' in chord_details[1]:
            inversion = get_number(chord_details[1])
        else: #we have a chord shape
            shape = chord_details[1]
    elif len(chord_details) == 3:  # chord with inversion and alteration
        if 'inv' in chord_details[2]:
            inversion = get_number(chord_details[2])
        else: #we have a chord shape
            shape = chord_details[1]

    return get_chord(scale, base_note, inversion, shape)

def get_scale_note(scale, base_note, degree):
# returns the midi note id of the nth degree of a scale
    degree_sum =  sum(chord_families[scale]['scale'][:degree-1])
    nt = get_note_id(base_note)
    return nt+degree_sum

def get_scale_triad(scale, base_note, ascending=True):
# get the 1st, 3rd, 5th of a scale in ascending or descending fashion
    triad = []
    triad.append (get_scale_note(scale, base_note, 5))
    triad.append (get_scale_note(scale, base_note, 3))
    triad.append (get_scale_note(scale, base_note, 1))
    if ascending==True:
        triad = sorted(triad)
    return triad

def explore_scale(family, base_note, alternate_sequence=True, starting_sequence=0, base_scale_descending=False):
    # explores a chord family by playing triads (alternating or not) in a descending or ascending fashion
    scales = []
    filtered_scale = []
    base_scale = []
    base_note_id = get_note_id(base_note)
    for i, v in chord_families.items():
        if v['family']==family:
            scales.append(v['scale'])
            if v['degree'] == 1:
                base_scale = v['scale']

    #calculate base notes
    base_scale_notes= []
    base_scale_notes.append(base_note_id)
    base_scale_notes_further = [base_note_id + sum(base_scale[:i+1]) for i, x in enumerate(base_scale) if i<len(base_scale)-1]
    base_scale_notes= base_scale_notes+base_scale_notes_further
    if base_scale_descending == True:
        base_scale_notes = list(reversed(base_scale_notes))
        scales = list(reversed(scales))

    for i,a in enumerate(scales):
        if alternate_sequence==True and i%2 == starting_sequence: #make this descending
            filtered_scale.append(base_scale_notes[i]+sum(scales[i][:4]))
            filtered_scale.append(base_scale_notes[i]+sum(scales[i][:2]))
            filtered_scale.append(base_scale_notes[i])
        else:
            filtered_scale.append(base_scale_notes[i])
            filtered_scale.append(base_scale_notes[i]+sum(scales[i][:2]))
            filtered_scale.append(base_scale_notes[i]+sum(scales[i][:4]))

    return filtered_scale
