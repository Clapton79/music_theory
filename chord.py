class Chord:

    def __init__(self, chord: str):
        chord_parts = chord.split()
        #TODO: default case? error if len is not 2 or 3?
        if len(chord_parts) == 0:
            raise ValueError(f"Chord '{chord}' is empty!")
        # let's ignore longer inputs for now

        self.base_note = chord_parts[0]
        self.shape = "major"
        self.inversion = 0

        if 1 < len(chord_parts):
            if not chord_parts[1].startswith("inv"):
                self.shape = chord_parts[1]
            if chord_parts[-1].startswith("inv"):
                self.inversion = chord_parts[-1][-1] # last char of last item


    def __str__(self):
        return " ".join(filter(None, [self.base_note, self.shape, str(self.inversion)]))


# chord = Chord(" ")# error
# print(f"'{chord}'")

chord = Chord("C")
print(f"'{chord}'")

chord = Chord(" C ")
print(f"'{chord}'")

chord = Chord("C major")
print(f"'{chord}'")

chord = Chord("F# min7b5")
print(f"'{chord}'")

chord = Chord("G7 inv2")
print(f"'{chord}'")

chord = Chord("F# min7b5 inv1")
print(f"'{chord}'")
