from midiutil.MidiFile import MIDIFile

from utils import save_midi_file


def create_danseband_edm_template():
    # Create MIDI object with 6 tracks
    midi_file = MIDIFile(6)

    # Track 0: Steel Guitar melody line
    # Track 1: Bass line (typical danseband walking bass)
    # Track 2: Rhythm guitar/accordion chords
    # Track 3: Basic drum pattern
    # Track 4: EDM-style rhythmic elements
    # Track 5: Pad/atmosphere track for EDM elements

    # Global settings
    tempo = 128  # Good compromise between danseband and EDM
    time = 0

    for track in range(6):
        midi_file.addTempo(track, time, tempo)
        midi_file.addProgramChange(track, 0, time, get_instrument(track))

    # Basic chord progression (I-IV-V-I in C major)
    chords = [(60, 64, 67), (65, 69, 72), (67, 71, 74), (60, 64, 67)]

    # Steel Guitar Melody (Track 0)
    create_steel_guitar_melody(midi_file, 0, chords)

    # Bass Line (Track 1)
    create_bass_pattern(midi_file, 1, chords)

    # Rhythm Section (Track 2)
    create_rhythm_section(midi_file, 2, chords)

    # Basic Drums (Track 3)
    create_drum_pattern(midi_file, 3)

    # EDM Elements (Track 4)
    create_edm_rhythm(midi_file, 4)

    # Atmospheric Pads (Track 5)
    create_atmosphere(midi_file, 5, chords)

    save_midi_file(midi_file, "danseband_edm_template.mid")


def get_instrument(track):
    instruments = {
        0: 25,  # Steel Guitar
        1: 33,  # Electric Bass
        2: 22,  # Accordion
        3: 0,  # Standard Kit
        4: 81,  # Synth Lead
        5: 91,  # Pad
    }
    return instruments.get(track, 0)


def create_steel_guitar_melody(midi_file, track, chords):
    # Create a simple melodic pattern based on chord tones
    duration = 1
    for bar in range(4):
        for note in chords[bar]:
            midi_file.addNote(track, 0, note, bar * 4, duration, 100)
            midi_file.addNote(track, 0, note + 12, bar * 4 + 2, duration, 80)


def create_bass_pattern(midi_file, track, chords):
    # Traditional walking bass pattern
    for bar in range(4):
        root = chords[bar][0] - 24  # Two octaves down
        midi_file.addNote(track, 0, root, bar * 4, 2, 100)
        midi_file.addNote(track, 0, root + 7, bar * 4 + 2, 2, 90)


def create_rhythm_section(midi_file, track, chords):
    # Typical danseband rhythm chord pattern
    for bar in range(4):
        for note in chords[bar]:
            midi_file.addNote(track, 0, note, bar * 4, 0.5, 70)
            midi_file.addNote(track, 0, note, bar * 4 + 1, 0.5, 70)
            midi_file.addNote(track, 0, note, bar * 4 + 2, 0.5, 70)
            midi_file.addNote(track, 0, note, bar * 4 + 3, 0.5, 70)


def create_drum_pattern(midi_file, track):
    # Basic drum pattern (using General MIDI drum map)
    kick = 36
    snare = 38
    hihat = 42

    # 4/4 pattern
    for bar in range(4):
        # Kick pattern
        midi_file.addNote(track, 9, kick, bar * 4, 1, 100)
        midi_file.addNote(track, 9, kick, bar * 4 + 2.5, 1, 100)

        # Snare on 2 and 4
        midi_file.addNote(track, 9, snare, bar * 4 + 1, 1, 90)
        midi_file.addNote(track, 9, snare, bar * 4 + 3, 1, 90)

        # Hi-hat pattern
        for beat in range(4):
            midi_file.addNote(track, 9, hihat, bar * 4 + beat, 0.5, 80)


def create_edm_rhythm(midi_file, track):
    # EDM-style rhythmic elements
    note = 60  # C4
    for bar in range(4):
        for eighth in range(8):
            if eighth % 3 == 0:  # Create a triplet feel
                midi_file.addNote(track, 0, note, bar * 4 + eighth * 0.5, 0.5, 90)


def create_atmosphere(midi_file, track, chords):
    # Sustained pad notes for atmosphere
    for bar in range(4):
        for note in chords[bar]:
            midi_file.addNote(track, 0, note, bar * 4, 4, 60)


if __name__ == "__main__":
    create_danseband_edm_template()
