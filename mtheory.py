import regex as re
# import itertools
# import collections

sound_sharps = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#','A', 'A#', 'B']
sound_flats = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

MIDI_C_NOTE = 12

chord_families = {
    'major'                 : { 'scale': [2,2,1,2,2,2,1], 'degree': 1, 'family' : 'major' },
    'dorian'                : { 'scale': [2,1,2,2,2,1,2], 'degree': 2, 'family' : 'major' },
    'phrygian'              : { 'scale': [1,2,2,2,1,2,2], 'degree': 3, 'family' : 'major' },
    'lidyan'                : { 'scale': [2,2,2,1,2,2,1], 'degree': 4, 'family' : 'major' },
    'mixolydian'            : { 'scale': [2,2,1,2,2,1,2], 'degree': 5, 'family' : 'major' },
    'natural minor'         : { 'scale': [2,1,2,2,1,2,2], 'degree': 6, 'family' : 'major' },
    'locrian'               : { 'scale': [1,2,2,1,2,2,2], 'degree': 7, 'family' : 'major' },
 
    'melodic minor'         : { 'scale': [2,1,2,2,1,2,2], 'degree': 1, 'family': 'melodic minor' },
    'dorian b2'             : { 'scale': [1,2,2,1,2,2,2], 'degree': 2, 'family': 'melodic minor' },
    'lydian augmented'      : { 'scale': [2,2,1,2,2,2,1], 'degree': 3, 'family': 'melodic minor' },
    'lydian dominant'       : { 'scale': [2,1,2,2,2,1,2], 'degree': 4, 'family': 'melodic minor' },
    'aeolian dominant'      : { 'scale': [1,2,2,2,1,2,2], 'degree': 5, 'family': 'melodic minor' },
    'half diminished'       : { 'scale': [2,2,2,1,2,2,1], 'degree': 6, 'family': 'melodic minor' },
    'altered'               : { 'scale': [2,2,1,2,2,1,2], 'degree': 7, 'family': 'melodic minor' },
 
    'harmonic minor'        : { 'scale': [2,1,2,2,1,3,1], 'degree': 1, 'family': 'harmonic minor' },
    'locrian natural 6'     : { 'scale': [1,2,2,1,3,1,2], 'degree': 2, 'family': 'harmonic minor' },
    'major #5'              : { 'scale': [2,2,1,3,1,2,1], 'degree': 3, 'family': 'harmonic minor' },
    'dorian #4'             : { 'scale': [2,1,3,1,2,1,2], 'degree': 4, 'family': 'harmonic minor' },
    'phrygian dominant'     : { 'scale': [1,3,1,2,1,2,2], 'degree': 5, 'family': 'harmonic minor' },
    'lydian #2'             : { 'scale': [3,1,2,1,2,2,1], 'degree': 6, 'family': 'harmonic minor' },
    'altered dominant bb7'  : { 'scale': [1,2,1,2,2,1,3], 'degree': 7, 'family': 'harmonic minor' },
 
    'harmonic major'        : { 'scale': [2,2,1,2,1,3,1], 'degree': 1, 'family': 'harmonic major' },
    'dorian b5'             : { 'scale': [2,1,2,1,3,1,2], 'degree': 2, 'family': 'harmonic major' },
    'phrygian b4'           : { 'scale': [1,2,1,3,1,2,2], 'degree': 3, 'family': 'harmonic major' },
    'lydian b3'             : { 'scale': [2,1,3,1,2,2,1], 'degree': 4, 'family': 'harmonic major' },
    'mixolydian b2'         : { 'scale': [1,3,1,2,2,1,2], 'degree': 5, 'family': 'harmonic major' },
    'lydian augmented'      : { 'scale': [3,1,2,2,1,2,1], 'degree': 6, 'family': 'harmonic major' },
    'locrian bb7'           : { 'scale': [1,2,2,1,2,1,3], 'degree': 7, 'family': 'harmonic major' },
 
    'diminished'            : { 'scale': [2,1,2,1,2,1,2], 'degree': 1, 'family': 'diminished' },
    'inverted diminished'   : { 'scale': [1,2,1,2,1,2,1], 'degree': 2, 'family': 'diminished' },
  
    'whole tone'            : { 'scale': [2,2,2,2,2],     'degree': 1, 'family': 'whole tone' },
  
    'augmented'             : { 'scale': [3,1,3,1,3,1],   'degree': 1, 'family': 'augmented' },
    'inverted augmented'    : { 'scale': [1,3,1,3,1,3],   'degree': 2, 'family': 'augmented' }
}

chord_shapes = {
    'major'  : ['1', '3', '5'],
    'maj7'   : ['1', '3', '5', '7'],
    'm7'     : ['1', 'b3', '5', 'b7'],
    '7'      : ['1', '3', '5', '7'],
    'm7b5'   : ['1', 'b3', 'b5', 'b7'],
    'm7#5'   : ['1', 'b3', '#5', 'b7'],
    'm7#5b9' : ['1', 'b3', '#5', 'b7', 'b9'],
    'm7#5#9' : ['1', 'b3', '#5', 'b7', '#9'],
    'm7b5#9' : ['1', 'b3', 'b5', 'b7', '#9'],
    'm7b9'   : ['1', '3', '5', 'b7', 'b9'],
    'm7b5b9' : ['1', 'b3', 'b5', 'b7', 'b9'],
    '7b5#9'  : ['1', '3', 'b5', 'b7', '#9'],
    '7#9b13' : ['1', '3', 'b5', 'b7', '#9', 'b13'],
    'sus4'   : ['1', '3', '4'],
    'maj7b5' : ['1', '3', 'b5', '7'],
    'min'    : ['1', 'b3', '5'],
    'minb5'  : ['1', 'b3', 'b5'],
    'min7'   : ['1', 'b3', '5', 'b7'],
    'min7b5' : ['1', 'b3', 'b5', 'b7'],
    'add9'   : ['1', '3', '5', '9'],
    'add13'  : ['1', '3', '5', '13'],
    'add9/11': ['1', '3', '5', '11'],
    'sus2'   : ['1', '2', '5'],
    'sus4'   : ['1', '4', '5'],
    'dim'    : ['1', 'b3', 'b5', '#9']
}

#TODO: not in use
progression_degrees = {
    'I'   : { 'degree': 1, 'equivalent': 'major' },
    'II'  : { 'degree': 2, 'equivalent': 'major' },
    'III' : { 'degree': 3, 'equivalent': 'major' },
    'IV'  : { 'degree': 4, 'equivalent': 'major' },
    'V'   : { 'degree': 5, 'equivalent': 'major' },
    'VI'  : { 'degree': 6, 'equivalent': 'major' },
    'VII' : { 'degree': 7, 'equivalent': 'major' },
    'VIII': { 'degree': 8, 'equivalent': 'major' },
    'i'   : { 'degree': 1, 'equivalent': 'minor' },
    'ii'  : { 'degree': 2, 'equivalent': 'minor' },
    'iii' : { 'degree': 3, 'equivalent': 'minor' },
    'iv'  : { 'degree': 4, 'equivalent': 'minor' },
    'v'   : { 'degree': 5, 'equivalent': 'minor' },
    'vi'  : { 'degree': 6, 'equivalent': 'minor' },
    'vii' : { 'degree': 7, 'equivalent': 'minor' },
    'viii': { 'degree': 8, 'equivalent': 'minor' }
}


def explore_scale(family, base_note, alternate_sequence = True, starting_sequence = 0, base_scale_descending = False):
    """Explores a chord family by playing triads (alternating or not) in a descending or ascending fashion."""
    filtered_scale = []
    scales = []
    base_scale = []
    base_midi_note_id = _get_midi_note_id(base_note)

    for i, v in chord_families.items():
        if v['family'] == family:
            scales.append(v['scale'])
            if v['degree'] == 1:
                base_scale = v['scale']

    #calculate base notes
    base_scale_notes = []
    base_scale_notes.append(base_midi_note_id)
    base_scale_notes_further = [base_midi_note_id + sum(base_scale[:i + 1]) for i, x in enumerate(base_scale) if i < len(base_scale) - 1]
    base_scale_notes.extend(base_scale_notes_further)

    if base_scale_descending == True:
        base_scale_notes = list(reversed(base_scale_notes))
        scales = list(reversed(scales))

    for i, a in enumerate(scales):
        if alternate_sequence == True and i % 2 == starting_sequence: # make this descending
            filtered_scale.append(base_scale_notes[i] + sum(scales[i][:4]))
            filtered_scale.append(base_scale_notes[i] + sum(scales[i][:2]))
            filtered_scale.append(base_scale_notes[i])
        else:
            filtered_scale.append(base_scale_notes[i])
            filtered_scale.append(base_scale_notes[i] + sum(scales[i][:2]))
            filtered_scale.append(base_scale_notes[i] + sum(scales[i][:4]))

    return filtered_scale


def _get_chord_info(chord):
    """Breaks down a chord into parts, then looks up its notes."""
    chord_details = chord.split(' ')
    #defaults
    shape = 'major'
    scale = 'major'
    inversion = 0
    base_note = chord_details[0]

    if len(chord_details) == 2:         # chord with alteration OR inversion
        if 'inv' in chord_details[1]:
            inversion = _get_note_octave(chord_details[1])
        else: # we have a chord shape
            shape = chord_details[1]
    elif len(chord_details) == 3:       # chord with inversion AND alteration
        if 'inv' in chord_details[2]:
            inversion = _get_note_octave(chord_details[2])
        else: # we have a chord shape
            shape = chord_details[1]

    return _get_chord(scale, base_note, inversion, shape)


def _get_chord(scale='major', base_note= 'C1', inversion=0, shape = 'major', add_bass = False, bass_degree = 1):
    """Returns a list of chord sounds for a scale and base note."""
    base_note_id = _get_midi_note_id(base_note)

    if inversion > 3 or inversion < 0:
        raise ValueError('Invalid inversion')
    scale_notes = _get_scale(scale, base_note_id, 2)

    if len(scale_notes) == 0:
        return []
    else:
        degrees, alteration = _get_chord_shapes(shape)
        chord = [scale_notes[a - 1] for a in degrees]
        chord = [a + alteration[i] for i, a in enumerate(chord)]

    if inversion == 1:
        chord[0] += MIDI_C_NOTE
    elif inversion == 2:
        chord[0] += MIDI_C_NOTE
        chord[1] += MIDI_C_NOTE

    if add_bass:
        bass_note_id = base_note_id - MIDI_C_NOTE    # bass note defaults to an octave lower
        if bass_degree == 1:
            bass_note_id = base_note_id - MIDI_C_NOTE
        else:
            bass_scale = _get_scale(scale, bass_note_id)
            bass_note_id = bass_scale[bass_degree - 1]
        chord.append(bass_note_id)

    return sorted(chord)


def _get_chord_shapes(shape):
    """Returns a list of what degrees and what alterations a chord has."""
    try:
        degrees = [_get_note_octave(x) for x in chord_shapes[shape]]
        alterations = []
        alt = [_get_note_base(x) for x in chord_shapes[shape]]
        for a in alt:
            if a == '':
                alterations.append(0)
            if a == 'b': # flat
                alterations.append(-1)
            if a == '#': # sharp
                alterations.append(1)
        return degrees, alterations
    except IndexError:
        return [], []
    except KeyError:
        return [], []


def _get_scale(scale, base_note = 60, octaves = 1, close_with_base = False, reverse = False):
    """Returns a list of notes for a scale."""
    try:
        degrees = [x['scale'] for i, x in chord_families.items() if i == scale][0]
        if octaves > 1:
            result = []
            for o in range(octaves):
                result += _get_scale(scale, base_note + (MIDI_C_NOTE * o), 1, close_with_base, reverse)
        else:
            result = [base_note + sum(degrees[:i]) for i, x in enumerate(degrees)]

        if close_with_base == True:
            result.append(base_note + (MIDI_C_NOTE * octaves))

        if reverse == True:
            result.reverse()

        return result
#TODO: should not happen, investigate how to prevent it
    except IndexError:
        return []


def _get_midi_note_id(note: str):
    """Returns the MIDI note ID."""
    note_index = _get_note_index(_get_note_base(note))
    note_octave = _get_note_octave(note)
#TODO: why do we start with MIDI_C_NOTE here? (is it (note_octave + 1) * MIDI_C_NOTE + note_index), but why?
    midi_note_id = MIDI_C_NOTE + note_index + note_octave * MIDI_C_NOTE
    return midi_note_id


def _get_note_index(note: str):
    """Finds the index of a note in the list of sounds."""
    if note not in sound_sharps and note not in sound_flats:
        raise ValueError(f"Note '{note}' does not exist!")
    if note in sound_sharps:
        return sound_sharps.index(note)
    elif note in sound_flats:
        return sound_flats.index(note)


def _get_note_octave(note: str) -> int:
    """Returns only the octave of the note."""
    try:
        return int(re.sub('[^\-0-9]', '', note))
    except:
#TODO: why the default 4? should validate the incoming note
        return 4


def _get_note_base(note: str) -> str:
    """Returns only the base note of a sound."""
#TODO: should validate the incoming note
    return re.sub('[\-0-9]', '', note)


#TODO: not in use | public?
def __get_list_note_ids(notes):
    """Returns up the midi note ID's of a list of notes."""
    note_ids = []
    for note in notes:
        note_ids.append(_get_midi_note_id(note))
    return note_ids


#TODO: not in use | public?
def __get_scale_triad(scale, base_note, ascending = True):
    """Gets the 1st, 3rd, 5th of a scale in ascending or descending fashion."""
    triad = []
#TODO: why in this desc order? does it matter?
    triad.append(__get_scale_note(scale, base_note, 5))
    triad.append(__get_scale_note(scale, base_note, 3))
    triad.append(__get_scale_note(scale, base_note, 1))
    if ascending == True:
        triad = sorted(triad)
    return triad


#TODO: not in use
def __get_chord_notes(chord):
    """Returns the list of notes in a chord."""
    return [get_note(x) for x in _get_chord_info(chord)]


#TODO: not in use
def __get_note(note_id, use_flat = False, with_octaves = False):
    """
    Returns the midi note ID for a note by calculating the difference from the base C note
    and make the steps using the note arrays.
    """
    diff = (note_id - MIDI_C_NOTE) % MIDI_C_NOTE
    if with_octaves == False:
        return sound_flats[diff] if use_flat else sound_sharps[diff]
    else:
        return sound_flats[diff] + str(int(round(note_id / 12, 0))) if use_flat else sound_sharps[diff] + str(int(round(note_id / 12, 0)))


#TODO: not in use
def __get_scale_note(scale, base_note, degree):
    """Returns the midi note ID of the Nth degree of a scale."""
    degree_sum = sum(chord_families[scale]['scale'][:degree - 1])
    note_id = _get_midi_note_id(base_note)
    return note_id + degree_sum
