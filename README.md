# Music theory project

This project intends to help with music theory: display and play scales,
create simple midi format sound files a guitarist can practice with.

Later I will include features that help connecting scales over chord
progressions.

## Methods

| package      | method                | description                                                                                                               | remark     |
| ------------ | --------------------- | ------------------------------------------------------------------------------------------------------------------------- | ---------- |
| music_theory | explore_scale         | Explores a chord family by playing triads (alternating or not) in a descending or ascending fashion.                      | public     |
|              | get_chord_info        | Breaks down a chord into parts, then looks up its notes. eg. input: 'F# min7b5 inv1'.                                     | private    |
|              | \_get_chord           | Returns a list of chord sounds for a scale and base note.                                                                 | private    |
|              | \_get_chord_shapes    | Returns a list of what degrees and what alterations a chord has.                                                          | private    |
|              | \_get_scale           | Returns a list of notes for a scale.                                                                                      | private    |
|              | \_get_midi_note_id    | Returns the MIDI note ID.                                                                                                 | private    |
|              | \_get_note_index      | Returns the index of a note in the list of notes.                                                                         | private    |
|              | \_get_note_octave     | Returns only the octave of the note.                                                                                      | private    |
|              | \_get_note_base       | Removes numbers from a text.                                                                                              | private    |
|              | \_\_get_list_note_ids | Returns up the midi note ID's of a list of notes.                                                                         | not in use |
|              | \_\_get_scale_triad   | Gets the 1st, 3rd, 5th of a scale in ascending or descending fashion.                                                     | not in use |
|              | \_\_get_chord_notes   | Returns the list of notes in a chord.                                                                                     | not in use |
|              | \_\_get_note          | Returns the midi note ID for a note by calculating the difference from the base C note and make the steps using the note. | not in use |
|              | \_\_get_scale_note    | Returns the midi note ID of the Nth degree of a scale. arrays.                                                            | not in use |
| midi helper  | create music          | creates a music file from a list of note id's                                                                             |            |
|              | play_music            | plays a midi files                                                                                                        |            |
|              | create_music_chords   | creates a music file from a list of chords                                                                                |            |

## Build-up of a chord:

example: `C# m7b5 inv2`

| sample | description                |
| ------ | -------------------------- |
| `C#`   | name of _root note_        |
| `m7b5` | _alterations_ to the chord |
| `inv2` | _inversions_ (1st or 2nd)  |

## Dev dependencies

### Virtual Environment

    pipenv install

### Packages

    pip3 install regex
    pip3 install MIDIUtil
    pip3 install -U pygame --user
