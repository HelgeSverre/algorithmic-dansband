import math

from midiutil.MidiFile import MIDIFile

from utils import save_midi_file


def setup_track_names(midi_file):
    """Setup proper track names for better MIDI organization"""
    track_names = {
        0: "Tenor Sax",
        1: "Accordion",
        2: "Bass",
        3: "Rhythm Guitar",
        4: "Drums",
        5: "Lead Vocal",
        6: "Alto Sax",
    }
    for track, name in track_names.items():
        midi_file.addTrackName(track, 0, name)


def create_angels_progression():
    """Create the actual chord progression from Jag trodde änglarna fans"""
    # In G major, following the sheet music
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
        [(67, 71, 74), (67, 71, 74)],  # G    G
    ]

    return verse_progression, chorus_progression


def create_angels_template():
    """Create MIDI arrangement of Jag trodde änglarna fans"""
    midi_file = MIDIFile(7, adjust_origin=False, deinterleave=False)
    setup_track_names(midi_file)

    # Global settings from sheet music
    tempo = 120  # As marked
    time = 0
    PPQN = 480  # Pulses per quarter note - higher for better triplet resolution

    # Song sections (in 12/8 bars)
    VERSE_LENGTH = 16
    CHORUS_LENGTH = 16

    # Initialize all tracks
    for track in range(7):
        midi_file.addTempo(track, time, tempo)
        midi_file.addControllerEvent(track, 0, 0, 7, get_initial_volume(track))
        midi_file.addControllerEvent(track, 0, 0, 10, get_pan_position(track))
        midi_file.addProgramChange(track, 0, time, get_instrument(track))

    verse_prog, chorus_prog = create_angels_progression()

    # Create full song structure following sheet music
    current_bar = 0

    # First verse
    create_verse_section(midi_file, current_bar, verse_prog, "first")
    current_bar += VERSE_LENGTH

    # Chorus
    create_chorus_section(midi_file, current_bar, chorus_prog, "first")
    current_bar += CHORUS_LENGTH

    # Second verse
    create_verse_section(midi_file, current_bar, verse_prog, "second")
    current_bar += VERSE_LENGTH

    # Final Chorus
    create_chorus_section(midi_file, current_bar, chorus_prog, "final")

    save_midi_file(midi_file, "jag_trodde_anglarna_fans_2.mid")


def create_verse_section(midi_file, start_bar, progression, verse_type):
    """Create verse arrangement with correct 12/8 timing"""
    for bar_pair in range(len(progression)):
        chord_pair = progression[bar_pair]
        for i in range(2):
            current_bar = start_bar + (bar_pair * 2) + i
            current_chord = chord_pair[i]
            next_chord = (
                chord_pair[1]
                if i == 0
                else progression[(bar_pair + 1) % len(progression)][0]
            )

            # In 12/8, each bar is divided into 4 main beats, each with 3 subdivisions
            create_full_12_8_bar(
                midi_file, current_chord, next_chord, current_bar, f"verse_{verse_type}"
            )


def create_rhythm_section_12_8(midi_file, chord, next_chord, bar, section_type):
    """Create rhythm section patterns in 12/8"""
    # Bass pattern: Quarter note + eighth note pattern
    root = chord[0] - 24
    fifth = chord[2] - 24

    bass_pattern = [
        (root, 1.0, 100),  # Quarter note
        (fifth, 0.5, 85),  # Eighth note
        (root, 1.0, 90),  # Quarter note
        (fifth, 0.5, 85),  # Eighth note
    ]

    time = bar * 4
    for note, duration, velocity in bass_pattern:
        midi_file.addNote(2, 0, note, time, duration, velocity)
        time += duration


def create_melody_12_8(midi_file, chord, bar, section_type):
    """Create vocal melody in 12/8 time following sheet music"""
    if not section_type.startswith("verse"):
        return

    # First phrase "jag trodde änglarna fans"
    melody = [
        (71, 0.33, 100),  # B
        (71, 0.33, 95),  # B
        (71, 0.33, 90),  # B
        (69, 0.33, 95),  # A
        (67, 0.33, 90),  # G
        (69, 0.33, 95),  # A
        (71, 0.33, 100),  # B
        (72, 0.33, 95),  # C
        (74, 1.0, 100),  # D (longer note)
    ]

    time = bar * 4
    for note, duration, velocity in melody:
        midi_file.addNote(5, 0, note, time, duration, velocity)
        add_vocal_expression(midi_file, 5, time, duration)
        time += duration


def add_vocal_expression(midi_file, track, start_time, duration):
    """Add realistic vocal expression"""
    steps = int(duration * 32)
    for i in range(steps):
        time = start_time + (i * duration / steps)
        # Add gentle vibrato
        value = 64 + int(math.sin(i * math.pi / 8) * 20)
        midi_file.addControllerEvent(track, 0, time, 1, value)


def create_accompaniment_12_8(midi_file, chord, bar, section_type):
    """Create accordion and guitar accompaniment in 12/8"""
    # Accordion pattern
    for beat in range(4):
        time = bar * 4 + beat
        # Play chord on each main beat
        for note in chord:
            midi_file.addNote(1, 0, note, time, 0.75, 85)


def get_initial_volume(track):
    """Volume levels following the sheet music dynamics"""
    volumes = {
        0: 85,  # Tenor Sax
        1: 90,  # Accordion
        2: 95,  # Bass
        3: 85,  # Rhythm Guitar
        4: 90,  # Drums
        5: 100,  # Lead Vocal
        6: 80,  # Alto Sax
    }
    return volumes.get(track, 90)


def get_pan_position(track):
    """Standard stereo positioning"""
    positions = {
        0: 70,  # Tenor Sax (slightly right)
        1: 58,  # Accordion (slightly left)
        2: 64,  # Bass (center)
        3: 54,  # Rhythm Guitar (slightly left)
        4: 64,  # Drums (center)
        5: 64,  # Lead Vocal (center)
        6: 74,  # Alto Sax (more right)
    }
    return positions.get(track, 64)


def get_instrument(track):
    """MIDI instruments closely matching Ole Ivars sound"""
    instruments = {
        0: 67,  # Tenor Sax
        1: 21,  # Accordion
        2: 34,  # Electric Bass
        3: 25,  # Acoustic Guitar
        4: 0,  # Standard Kit
        5: 53,  # Voice "Aah"
        6: 66,  # Alto Sax
    }
    return instruments.get(track, 0)


def create_chorus_section(midi_file, start_bar, progression, chorus_type):
    """Create chorus arrangement with proper phrasing"""
    for bar_pair in range(len(progression)):
        chord_pair = progression[bar_pair]
        for i in range(2):
            current_bar = start_bar + (bar_pair * 2) + i
            current_chord = chord_pair[i]
            next_chord = (
                chord_pair[1]
                if i == 0
                else progression[(bar_pair + 1) % len(progression)][0]
            )

            create_full_12_8_bar(
                midi_file,
                current_chord,
                next_chord,
                current_bar,
                f"chorus_{chorus_type}",
                intensity=1.1 if chorus_type == "final" else 1.0,
            )


def create_full_12_8_bar(
    midi_file, chord, next_chord, bar, section_type, intensity=1.0
):
    """Create a full bar arrangement in 12/8 time"""
    # Base timing for 12/8
    beat_duration = 1.0
    triplet_duration = beat_duration / 3.0

    # Create individual instrument patterns
    create_bass_pattern_12_8(midi_file, chord, next_chord, bar, intensity)
    create_guitar_pattern_12_8(midi_file, chord, bar, intensity)
    create_drums_12_8(midi_file, bar, section_type, intensity)
    create_accordion_pattern_12_8(midi_file, chord, bar, section_type, intensity)

    if section_type.startswith("chorus"):
        create_chorus_melody(midi_file, chord, bar, section_type)
        create_sax_chorus_pattern(midi_file, chord, bar, intensity)


def create_bass_pattern_12_8(midi_file, chord, next_chord, bar, intensity=1.0):
    """Create bass pattern with proper 12/8 walking line"""
    root = chord[0] - 24
    fifth = chord[2] - 24
    next_root = next_chord[0] - 24
    base_velocity = int(95 * intensity)

    # Main pattern (following sheet music rhythm)
    pattern = [
        (root, 1.0, base_velocity),  # Beat 1: root (quarter note)
        (fifth, 0.5, base_velocity - 10),  # Beat 1+: fifth (eighth note)
        (root, 1.0, base_velocity - 5),  # Beat 2: root (quarter note)
        (fifth, 0.5, base_velocity - 10),  # Beat 2+: fifth (eighth note)
        (root, 0.5, base_velocity - 5),  # Beat 3: walking pattern to next chord
        (root + 2, 0.5, base_velocity - 10),
    ]

    time = bar * 4
    for note, duration, velocity in pattern:
        midi_file.addNote(2, 0, note, time, duration, velocity)
        time += duration


def create_guitar_pattern_12_8(midi_file, chord, bar, intensity=1.0):
    """Create rhythm guitar pattern with proper 12/8 strumming"""
    base_velocity = int(85 * intensity)

    # Typical dansband guitar pattern in 12/8
    for beat in range(4):
        time = bar * 4 + beat

        # Down strum on the beat
        for note in chord:
            midi_file.addNote(3, 0, note, time, 0.3, base_velocity)

        # Up strum on the off-beat
        for note in chord:
            midi_file.addNote(3, 0, note, time + 0.5, 0.2, base_velocity - 10)


def create_drums_12_8(midi_file, bar, section_type, intensity=1.0):
    """Create drum pattern with proper 12/8 feel"""
    kick = 36
    snare = 38
    hihat = 42
    crash = 49

    base_velocity = int(90 * intensity)

    # Basic pattern
    time = bar * 4

    # Kick drum pattern
    midi_file.addNote(4, 9, kick, time, 0.5, base_velocity)
    midi_file.addNote(4, 9, kick, time + 2, 0.5, base_velocity - 5)

    # Snare on 2 and 4
    midi_file.addNote(4, 9, snare, time + 1, 0.5, base_velocity)
    midi_file.addNote(4, 9, snare, time + 3, 0.5, base_velocity)

    # Hi-hat pattern (12/8 triplet feel)
    for i in range(12):
        midi_file.addNote(4, 9, hihat, time + (i * 0.333), 0.3, base_velocity - 20)


def create_accordion_pattern_12_8(midi_file, chord, bar, section_type, intensity=1.0):
    """Create accordion pattern with characteristic 12/8 feel"""
    base_velocity = int(90 * intensity)

    # Main chord pattern
    time = bar * 4
    for beat in range(4):
        # Full chord on the beat
        for note in chord:
            midi_file.addNote(1, 0, note, time + beat, 0.75, base_velocity)

        # Upper voices on off-beats for fill
        if beat % 2 == 1:
            midi_file.addNote(
                1, 0, chord[1], time + beat + 0.5, 0.25, base_velocity - 15
            )
            midi_file.addNote(
                1, 0, chord[2], time + beat + 0.5, 0.25, base_velocity - 15
            )


def create_chorus_melody(midi_file, chord, bar, section_type):
    """Create chorus vocal melody following sheet music"""
    # Chorus melody "nu har jag en ängel här hos mig"
    if not section_type.startswith("chorus"):
        return

    melody = [
        (74, 0.5, 100),  # D
        (72, 0.5, 95),  # C
        (71, 0.5, 95),  # B
        (69, 0.5, 90),  # A
        (67, 1.0, 100),  # G
        (69, 1.0, 95),  # A
    ]

    time = bar * 4
    for note, duration, velocity in melody:
        midi_file.addNote(5, 0, note, time, duration, velocity)
        add_vocal_expression(midi_file, 5, time, duration)
        time += duration


def create_sax_chorus_pattern(midi_file, chord, bar, intensity=1.0):
    """Create saxophone harmony parts for chorus"""
    base_velocity = int(85 * intensity)

    # Tenor sax
    for note in [chord[1], chord[2]]:  # Third and fifth
        midi_file.addNote(0, 0, note + 12, bar * 4, 2.0, base_velocity - 10)
        add_sax_expression(midi_file, 0, bar * 4, 2.0)

    # Alto sax
    midi_file.addNote(6, 0, chord[2] + 24, bar * 4, 2.0, base_velocity - 15)
    add_sax_expression(midi_file, 6, bar * 4, 2.0)


def add_sax_expression(midi_file, track, start_time, duration):
    """Add realistic saxophone expression"""
    steps = int(duration * 32)
    vibrato_speed = 5.5
    depth = 15

    for i in range(steps):
        time = start_time + (i * duration / steps)
        # Gentle vibrato
        value = 64 + int(math.sin(2 * math.pi * vibrato_speed * i / steps) * depth)
        midi_file.addControllerEvent(track, 0, time, 1, value)


if __name__ == "__main__":
    create_angels_template()
