import math

from midiutil.MidiFile import MIDIFile

from utils import save_midi_file


def setup_track_names(midi_file):
    """Setup proper track names for better MIDI organization"""
    track_names = {0: "Lead Vocal", 1: "Backing Track"}
    for track, name in track_names.items():
        midi_file.addTrackName(track, 0, name)


def create_angels_progression():
    """Create chord progression from Jag trodde änglarna fans"""
    # In G major
    verse_progression = [
        [(67, 71, 74), (67, 71, 74)],  # G    G
        [(72, 76, 79), (72, 76, 79)],  # C    C
        [(74, 78, 81), (74, 78, 81)],  # D    D
        [(67, 71, 74), (67, 71, 74)],  # G    G
        [(72, 76, 79), (74, 78, 81)],  # C    D
        [(64, 67, 71), (72, 76, 79)],  # Em   C
        [(67, 71, 74), (74, 78, 81)],  # G/D  D
    ]

    chorus_progression = [
        [(67, 71, 74), (72, 76, 79)],  # G    C
        [(74, 78, 81), (74, 78, 81)],  # D    D
        [(72, 76, 79), (74, 78, 81)],  # C    D
        [(64, 67, 71), (72, 76, 79)],  # Em   C
        [(67, 71, 74), (74, 78, 81)],  # G/D  D
        [(67, 71, 74), (67, 71, 74)],  # G    G
    ]

    return verse_progression, chorus_progression


def create_angels_template():
    """Create MIDI file with focus on vocal melody"""
    # Create MIDI file with 2 tracks (vocal + minimal backing)
    midi_file = MIDIFile(2)
    setup_track_names(midi_file)

    # Global settings from sheet music
    tempo = 120
    time = 0

    # Initialize tracks
    for track in range(2):
        midi_file.addTempo(track, time, tempo)
        midi_file.addProgramChange(track, 0, time, get_instrument(track))
        midi_file.addControllerEvent(track, 0, time, 7, get_volume(track))

    verse_prog, chorus_prog = create_angels_progression()
    current_bar = 0

    # Create song structure
    create_verse(midi_file, current_bar, verse_prog, "first")
    current_bar += 14  # Adjust length based on actual progression

    create_chorus(midi_file, current_bar, chorus_prog, "first")
    current_bar += 12  # Adjust length based on actual progression

    create_verse(midi_file, current_bar, verse_prog, "second")
    current_bar += 14

    create_chorus(midi_file, current_bar, chorus_prog, "final")

    save_midi_file(midi_file, "jag_trodde_anglarna_vocal.mid")


def create_verse(midi_file, start_bar, progression, verse_type):
    """Create verse section focusing on vocal melody"""
    for bar_pair in range(len(progression)):
        for i in range(2):
            current_bar = start_bar + (bar_pair * 2) + i
            current_chord = progression[bar_pair][i]
            create_vocal_melody_ole_ivars(
                midi_file, 0, current_chord, current_bar, f"verse_{verse_type}"
            )
            create_minimal_backing(midi_file, 1, current_chord, current_bar)


def create_chorus(midi_file, start_bar, progression, chorus_type):
    """Create chorus section focusing on vocal melody"""
    for bar_pair in range(len(progression)):
        for i in range(2):
            current_bar = start_bar + (bar_pair * 2) + i
            current_chord = progression[bar_pair][i]
            create_vocal_melody_ole_ivars(
                midi_file, 0, current_chord, current_bar, f"chorus_{chorus_type}"
            )
            create_minimal_backing(midi_file, 1, current_chord, current_bar)


def create_vocal_melody_ole_ivars(midi_file, track, chord, bar, section_type):
    """Create exact vocal melody from Jag trodde änglarna fans"""
    base_velocity = 100

    if section_type.startswith("verse"):
        # First phrase: "jag trodde änglarna fans"
        if bar % 4 == 0:
            # Starting with pickup note
            add_vocal_note(
                midi_file, track, 67, bar * 4 - 0.5, 0.5, base_velocity
            )  # G (pickup "jag")
            add_vocal_note(
                midi_file, track, 71, bar * 4, 0.5, base_velocity
            )  # B ("trod")
            add_vocal_note(
                midi_file, track, 71, bar * 4 + 0.5, 0.5, base_velocity
            )  # B ("de")
            add_vocal_note(
                midi_file, track, 71, bar * 4 + 1.0, 0.5, base_velocity
            )  # B ("äng")
            add_vocal_note(
                midi_file, track, 69, bar * 4 + 1.5, 0.5, base_velocity
            )  # A ("lar")
            add_vocal_note(
                midi_file, track, 67, bar * 4 + 2.0, 0.5, base_velocity
            )  # G ("na")
            add_vocal_note(
                midi_file, track, 69, bar * 4 + 2.5, 0.5, base_velocity
            )  # A ("fans")

        # Second phrase: "bara bara i himmelen"
        elif bar % 4 == 1:
            add_vocal_note(
                midi_file, track, 71, bar * 4, 0.5, base_velocity
            )  # B ("ba")
            add_vocal_note(
                midi_file, track, 72, bar * 4 + 0.5, 0.5, base_velocity
            )  # C ("ra")
            add_vocal_note(
                midi_file, track, 74, bar * 4 + 1.0, 1.0, base_velocity
            )  # D ("ba")
            add_vocal_note(
                midi_file, track, 71, bar * 4 + 2.0, 0.5, base_velocity
            )  # B ("ra")
            add_vocal_note(
                midi_file, track, 69, bar * 4 + 2.5, 0.5, base_velocity
            )  # A ("i")
            add_vocal_note(
                midi_file, track, 67, bar * 4 + 3.0, 1.0, base_velocity
            )  # G ("him-me-len")

    elif section_type.startswith("chorus"):
        # "nu har jag en ängel här"
        if bar % 4 == 0:
            add_vocal_note(
                midi_file, track, 74, bar * 4, 0.5, base_velocity
            )  # D ("nu")
            add_vocal_note(
                midi_file, track, 72, bar * 4 + 0.5, 0.5, base_velocity
            )  # C ("har")
            add_vocal_note(
                midi_file, track, 71, bar * 4 + 1.0, 0.5, base_velocity
            )  # B ("jag")
            add_vocal_note(
                midi_file, track, 69, bar * 4 + 1.5, 0.5, base_velocity
            )  # A ("en")
            add_vocal_note(
                midi_file, track, 67, bar * 4 + 2.0, 1.0, base_velocity
            )  # G ("äng")
            add_vocal_note(
                midi_file, track, 69, bar * 4 + 3.0, 1.0, base_velocity
            )  # A ("el")


def add_vocal_note(midi_file, track, note, start_time, duration, velocity):
    """Add vocal note with characteristic Ole Ivars style"""
    midi_file.addNote(track, 0, note, start_time, duration, velocity)

    # Add slight pitch bend at start of longer notes
    if duration >= 1.0:
        steps = 8
        for i in range(steps):
            time = start_time + (i * 0.1 / steps)
            value = 8192 + int((1.0 - i / steps) * 512)
            midi_file.addPitchWheelEvent(track, 0, time, value)

    # Add vibrato on held notes
    if duration > 0.5:
        steps = int(duration * 32)
        for i in range(steps):
            time = start_time + (i * duration / steps)
            value = 64 + int(math.sin(i * math.pi / 4) * 20)
            midi_file.addControllerEvent(track, 0, time, 1, value)


def create_minimal_backing(midi_file, track, chord, bar):
    """Create minimal backing track to support the vocal"""
    velocity = 60  # Quiet backing
    # Just play the chord on beat 1 of each bar
    for note in chord:
        midi_file.addNote(track, 0, note, bar * 4, 4, velocity)


def get_instrument(track):
    """Get instrument numbers"""
    instruments = {
        0: 53,  # Voice "Aah" for lead vocal
        1: 0,  # Piano for minimal backing
    }
    return instruments.get(track, 0)


def get_volume(track):
    """Get volume levels"""
    volumes = {0: 100, 1: 60}  # Full volume for vocal  # Quiet backing track
    return volumes.get(track, 100)


if __name__ == "__main__":
    create_angels_template()
