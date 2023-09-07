import regex as re
# import itertools
# import collections
from typing import Tuple, List

from scaleorder import ScaleOrder
from chord import Chord

class MusicTheory(object):

    SOUND_SHARPS = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#','A', 'A#', 'B']
    SOUND_FLATS = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

    MIDI_C_NOTE = 12
    BASE_DEGREE_ID = 1
    PROPERTY_MAIN_FAMILY = 'main_family'
    PROPERTY_SCALE = 'scale'
    PROPERTY_DEGREE = 'degree'

    CHORD_FAMILIES = {             # scale - number of semitones
        'major'                 : { 'scale': [2,2,1,2,2,2,1], 'degree': 1, 'main_family' : 'major' },
        'dorian'                : { 'scale': [2,1,2,2,2,1,2], 'degree': 2, 'main_family' : 'major' },
        'phrygian'              : { 'scale': [1,2,2,2,1,2,2], 'degree': 3, 'main_family' : 'major' },
        'lydian'                : { 'scale': [2,2,2,1,2,2,1], 'degree': 4, 'main_family' : 'major' },
        'mixolydian'            : { 'scale': [2,2,1,2,2,1,2], 'degree': 5, 'main_family' : 'major' },
        'natural minor'         : { 'scale': [2,1,2,2,1,2,2], 'degree': 6, 'main_family' : 'major' },
        'locrian'               : { 'scale': [1,2,2,1,2,2,2], 'degree': 7, 'main_family' : 'major' },
    
        'melodic minor'         : { 'scale': [2,1,2,2,1,2,2], 'degree': 1, 'main_family': 'melodic minor' },
        'dorian b2'             : { 'scale': [1,2,2,1,2,2,2], 'degree': 2, 'main_family': 'melodic minor' },
        'lydian augmented'      : { 'scale': [2,2,1,2,2,2,1], 'degree': 3, 'main_family': 'melodic minor' },
        'lydian dominant'       : { 'scale': [2,1,2,2,2,1,2], 'degree': 4, 'main_family': 'melodic minor' },
        'aeolian dominant'      : { 'scale': [1,2,2,2,1,2,2], 'degree': 5, 'main_family': 'melodic minor' },
        'half diminished'       : { 'scale': [2,2,2,1,2,2,1], 'degree': 6, 'main_family': 'melodic minor' },
        'altered'               : { 'scale': [2,2,1,2,2,1,2], 'degree': 7, 'main_family': 'melodic minor' },
    
        'harmonic minor'        : { 'scale': [2,1,2,2,1,3,1], 'degree': 1, 'main_family': 'harmonic minor' },
        'locrian natural 6'     : { 'scale': [1,2,2,1,3,1,2], 'degree': 2, 'main_family': 'harmonic minor' },
        'major #5'              : { 'scale': [2,2,1,3,1,2,1], 'degree': 3, 'main_family': 'harmonic minor' },
        'dorian #4'             : { 'scale': [2,1,3,1,2,1,2], 'degree': 4, 'main_family': 'harmonic minor' },
        'phrygian dominant'     : { 'scale': [1,3,1,2,1,2,2], 'degree': 5, 'main_family': 'harmonic minor' },
        'lydian #2'             : { 'scale': [3,1,2,1,2,2,1], 'degree': 6, 'main_family': 'harmonic minor' },
        'altered dominant bb7'  : { 'scale': [1,2,1,2,2,1,3], 'degree': 7, 'main_family': 'harmonic minor' },
    
        'harmonic major'        : { 'scale': [2,2,1,2,1,3,1], 'degree': 1, 'main_family': 'harmonic major' },
        'dorian b5'             : { 'scale': [2,1,2,1,3,1,2], 'degree': 2, 'main_family': 'harmonic major' },
        'phrygian b4'           : { 'scale': [1,2,1,3,1,2,2], 'degree': 3, 'main_family': 'harmonic major' },
        'lydian b3'             : { 'scale': [2,1,3,1,2,2,1], 'degree': 4, 'main_family': 'harmonic major' },
        'mixolydian b2'         : { 'scale': [1,3,1,2,2,1,2], 'degree': 5, 'main_family': 'harmonic major' },
        'lydian augmented'      : { 'scale': [3,1,2,2,1,2,1], 'degree': 6, 'main_family': 'harmonic major' },
        'locrian bb7'           : { 'scale': [1,2,2,1,2,1,3], 'degree': 7, 'main_family': 'harmonic major' },
    
        'diminished'            : { 'scale': [2,1,2,1,2,1,2], 'degree': 1, 'main_family': 'diminished' },
        'inverted diminished'   : { 'scale': [1,2,1,2,1,2,1], 'degree': 2, 'main_family': 'diminished' },
    
        'whole tone'            : { 'scale': [2,2,2,2,2],     'degree': 1, 'main_family': 'whole tone' },
    
        'augmented'             : { 'scale': [3,1,3,1,3,1],   'degree': 1, 'main_family': 'augmented' },
        'inverted augmented'    : { 'scale': [1,3,1,3,1,3],   'degree': 2, 'main_family': 'augmented' }
    }

    CHORD_SHAPES = {
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
    PROGRESSION_DEGREES = {
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


    def __init__(self):
        pass


    def explore_scale(self, main_chord_family, base_note, starting_sequence = 0, alternate_sequence = True, scale_order: ScaleOrder = ScaleOrder.ASCENDING) -> []:
        """Explores a chord family by playing triads (alternating or not) in a descending or ascending fashion."""

        # get each relevant chord family by a main chord family
        filtered_chord_families = [MusicTheory.CHORD_FAMILIES[key] for key in MusicTheory.CHORD_FAMILIES if MusicTheory.CHORD_FAMILIES[key][MusicTheory.PROPERTY_MAIN_FAMILY] == main_chord_family]
        final_scale_semitones = self.__create_semitone_scales(filtered_chord_families, starting_sequence, alternate_sequence, scale_order)

        #TODO: we should not create the list of MIDI note IDs at this point, only the scale [now we loose the sharp/flat part too],
        # and have a separate class to convert it to MIDI notes
        base_midi_note_id = self.__get_midi_note_id(base_note)
        final_scale_notes = [base_midi_note_id + semitone for semitone in final_scale_semitones]
        return final_scale_notes


    def __create_semitone_scales(self, filtered_chord_families: [], starting_sequence: int = 0, alternate_sequence: bool = True,scale_order: ScaleOrder = ScaleOrder.ASCENDING):
        base_scale = []     # represents the intervals between notes in the base scale
        scales = []         # each scale for chords in a main chord family
        base_scale, scales = self.__get_base_scale_and_scales(filtered_chord_families, scale_order)
        #TODO: what happens if there is no scales with degree == 1?
        base_semitone_scale = self.__create_base_semitone_scale(base_scale)

        final_semitone_scales = []
        for idx, _ in enumerate(scales):
            if alternate_sequence == True and idx % 2 == starting_sequence: # make this descending
                final_semitone_scales.append(base_semitone_scale[idx] + sum(scales[idx][:4]))
                final_semitone_scales.append(base_semitone_scale[idx] + sum(scales[idx][:2]))
                final_semitone_scales.append(base_semitone_scale[idx])
            else:
                final_semitone_scales.append(base_semitone_scale[idx])
                final_semitone_scales.append(base_semitone_scale[idx] + sum(scales[idx][:2]))
                final_semitone_scales.append(base_semitone_scale[idx] + sum(scales[idx][:4]))
        return final_semitone_scales


    def __get_base_scale_and_scales(self, filtered_chord_families: [], scale_order: ScaleOrder = ScaleOrder.ASCENDING) -> Tuple[List[int], List[str]]:
        """Gets the 'scales' and the 'base scale'."""
        base_scale = []
        scales = []
        for chord_family in filtered_chord_families:
            scales.append(chord_family[MusicTheory.PROPERTY_SCALE])
            if chord_family[MusicTheory.PROPERTY_DEGREE] == MusicTheory.BASE_DEGREE_ID:
                base_scale = chord_family[MusicTheory.PROPERTY_SCALE]

        if scale_order == ScaleOrder.DESCENDING:
            #TODO: if there is a single scale in the list (as in the base_scale),
            #  then the order of the single array (here the base_scale) is changed! Is this intentional?
            base_scale.reverse()
            scales.reverse()

        return base_scale, scales


    def __create_base_semitone_scale(self, base_scale: []) -> []:
        base_semitone_scale = [sum(base_scale[:idx]) for idx, _ in enumerate(base_scale)]
        return base_semitone_scale


    def get_chord_info(self, chord_as_string: str):
        """
        Breaks down a chord into parts, then looks up its notes.
        eg. input: 'F# min7b5 inv1'
        """
        #defaults
        #TODO: base_note default is C1? -> see __get_chord(...) parameters
        #TODO: inversion default is 0? -> see __get_chord(...) parameters
        shape = 'major' #TODO: make it a fallback value if chord shape property is None in the Chord instance
        scale = 'major' #TODO: is this a parameter?
        
        #TODO: could get rid of this function and create the Chord inside __get_chord
        chord = Chord(chord_as_string)
        return self.__get_chord(self, chord)


#TODO:----------------------------------------------------------------------------


    # def __get_chord(self, scale = 'major', base_note = 'C1', inversion = 0, shape = 'major', add_bass = False, bass_degree = 1):
    #TODO: handle bass scale separately
    def __get_chord(self, chord: Chord, add_bass = False, bass_degree = 1):
        """Returns a list of chord sounds for a scale and base note."""
        base_note_id = self.__get_midi_note_id(chord.base_note)

        if chord.inversion < 0 or 3 < chord.inversion:
            raise ValueError('Invalid inversion')
        scale_notes = self.__get_scale(chord, base_note_id, 2)

        if len(scale_notes) == 0:
            return []
        else:
            degrees, alterations = self.__get_chord_shapes(chord.shape)
            chord = [scale_notes[degree - 1] for degree in degrees]
            chord = [note + alterations[idx] for idx, note in enumerate(chord)]

        if chord.inversion == 1:
            chord[0] += MusicTheory.MIDI_C_NOTE
        elif chord.inversion == 2:
            chord[0] += MusicTheory.MIDI_C_NOTE
            chord[1] += MusicTheory.MIDI_C_NOTE
        #TODO: what about 3rd inversion?

        if add_bass:
            bass_note_id = base_note_id - MusicTheory.MIDI_C_NOTE    # bass note defaults to an octave lower
            if bass_degree == 1:
                bass_note_id = base_note_id - MusicTheory.MIDI_C_NOTE
            else:
                bass_scale = self.__get_scale(chord.scale, bass_note_id)
                bass_note_id = bass_scale[bass_degree - 1]
            chord.append(bass_note_id)

        return sorted(chord)


    def __get_chord_shapes(self, shape):
        """Returns a list of what degrees and what alterations a chord has."""
        try:
            alterations = []
            alteration = [self.__get_note_base(note) for note in MusicTheory.CHORD_SHAPES[shape]]
            degrees = [self.__get_note_octave(note) for note in MusicTheory.CHORD_SHAPES[shape]]
            for alt in alteration:
                if alt == '':
                    alterations.append(0)
                if alt == 'b': # flat
                    alterations.append(-1)
                if alt == '#': # sharp
                    alterations.append(1)
            return degrees, alterations
        except IndexError:
            return [], []
        except KeyError:
            return [], []


    def __get_scale(self, scale, base_note = 60, octaves = 1, close_with_base = False, reverse = False):
        """Returns a list of notes for a scale."""
        try:
            degrees = [chord_family[MusicTheory.PROPERTY_SCALE] for i, chord_family in MusicTheory.CHORD_FAMILIES.items() if i == scale][0]
            if octaves > 1:
                result = []
                for octave in range(octaves):
                    result += self.__get_scale(scale, base_note + (MusicTheory.MIDI_C_NOTE * octave), 1, close_with_base, reverse)
            else:
                result = [base_note + sum(degrees[:i]) for i, _ in enumerate(degrees)]

            if close_with_base == True:
                result.append(base_note + (MusicTheory.MIDI_C_NOTE * octaves))

            if reverse == True:
                result.reverse()

            return result
        #TODO: should not happen, investigate how to prevent it
        except IndexError:
            return []


    def __get_midi_note_id(self, note: str) -> int:
        """Returns the MIDI note ID."""
        note_index = self.__get_note_index(self.__get_note_base(note))
        note_octave = self.__get_note_octave(note)
        #TODO: why do we start with MIDI_C_NOTE here? (is it (note_octave + 1) * MIDI_C_NOTE + note_index), but why?
        midi_note_id = MusicTheory.MIDI_C_NOTE + note_index + note_octave * MusicTheory.MIDI_C_NOTE
        return midi_note_id


    def __get_note_index(self, note: str) -> int:
        """Finds the index of a note in the list of sounds."""
        if note in MusicTheory.SOUND_SHARPS:
            return MusicTheory.SOUND_SHARPS.index(note)
        elif note in MusicTheory.SOUND_FLATS:
            return MusicTheory.SOUND_FLATS.index(note)
        else:
            raise ValueError(f"Note '{note}' does not exist!")


    def __get_note_octave(self, note: str) -> int:
        """Returns only the octave of the note."""
        try:
            return int(re.sub('[^\-0-9]', '', note))
        except:
        #TODO: why the default 4? should validate the incoming note
            return 4


    def __get_note_base(self, note: str) -> str:
        """Returns only the base note of a sound."""
        #TODO: should validate the incoming note
        return re.sub('[\-0-9]', '', note)


    #TODO: not in use | public?
    def __get_list_note_ids(self, notes) -> []:
        """Returns up the midi note ID's of a list of notes."""
        note_ids = []
        for note in notes:
            note_ids.append(self.__get_midi_note_id(note))
        return note_ids


    #TODO: not in use | public?
    def __get_scale_triad(self, scale, base_note, ascending = True) -> []:
        """Gets the 1st, 3rd, 5th of a scale in ascending or descending fashion."""
        triad = []
        #TODO: why in this desc order? does it matter?
        triad.append(self.__get_scale_note(scale, base_note, 5))
        triad.append(self.__get_scale_note(scale, base_note, 3))
        triad.append(self.__get_scale_note(scale, base_note, 1))
        if ascending == True:
            triad = sorted(triad)
        return triad


    #TODO: not in use
    def __get_chord_notes(self, chord) -> []:
        """Returns the list of notes in a chord."""
        return [self.__get_note(x) for x in self.__get_chord_info(chord)]


    #TODO: not in use
    def __get_note(self, note_id, use_flat = False, with_octaves = False):
        """
        Returns the midi note ID for a note by calculating the difference from the base C note
        and make the steps using the note arrays.
        """
        diff = (note_id - MusicTheory.MIDI_C_NOTE) % MusicTheory.MIDI_C_NOTE
        if with_octaves == False:
            return MusicTheory.SOUND_FLATS[diff] if use_flat else self.SOUND_SHARPS[diff]
        else:
            return MusicTheory.SOUND_FLATS[diff] + str(int(round(note_id / 12, 0))) if use_flat else MusicTheory.SOUND_SHARPS[diff] + str(int(round(note_id / 12, 0)))


    #TODO: not in use
    def __get_scale_note(self, scale, base_note, degree):
        """Returns the midi note ID of the Nth degree of a scale."""
        degree_sum = sum(MusicTheory.CHORD_FAMILIES[scale][MusicTheory.PROPERTY_SCALE][:degree - 1])
        note_id = self.__get_midi_note_id(base_note)
        return note_id + degree_sum
