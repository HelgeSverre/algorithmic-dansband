from midiutil.MidiFile import MIDIFile
import math


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


def create_danseband_template():
    # Create MIDI object with 7 tracks (added Alto Sax)
    midi_file = MIDIFile(7, adjust_origin=False, deinterleave=False)

    # Add track names first
    setup_track_names(midi_file)

    # Global settings
    tempo = 128  # Typical dansband tempo
    time = 0

    # Song structure (in bars)
    INTRO_LENGTH = 4
    VERSE_LENGTH = 8
    CHORUS_LENGTH = 8
    BRIDGE_LENGTH = 4
    OUTRO_LENGTH = 4

    # Total song structure: Intro -> Verse -> Chorus -> Verse -> Chorus -> Bridge -> Chorus -> Outro
    TOTAL_BARS = (
        INTRO_LENGTH
        + (VERSE_LENGTH * 2)
        + (CHORUS_LENGTH * 3)
        + BRIDGE_LENGTH
        + OUTRO_LENGTH
    )

    # Initialize all tracks
    for track in range(7):
        midi_file.addTempo(track, time, tempo)
        midi_file.addControllerEvent(track, 0, 0, 7, get_initial_volume(track))
        midi_file.addControllerEvent(track, 0, 0, 10, get_pan_position(track))
        midi_file.addProgramChange(track, 0, time, get_instrument(track))

    setup_vocal_controls(midi_file, 5)
    setup_sax_controls(midi_file, 0)  # Setup sax instead of steel guitar

    # Typical dansband progression in D major (more common than D♭)
    base_chords = [
        (62, 66, 69),  # D major (D, F♯, A)
        (59, 62, 66),  # Bm (B, D, F♯)
        (67, 71, 74),  # G major (G, B, D)
        (69, 73, 76),  # A major (A, C♯, E)
    ]

    # Extended chord progressions for different sections
    verse_chords = base_chords * 2  # 8 bars
    chorus_chords = [
        (62, 66, 69),  # D
        (69, 73, 76),  # A
        (67, 71, 74),  # G
        (69, 73, 76),  # A
        (62, 66, 69),  # D
        (59, 62, 66),  # Bm
        (67, 71, 74),  # G
        (69, 73, 76),  # A
    ]
    bridge_chords = [
        (57, 61, 64),  # Am
        (62, 66, 69),  # D
        (67, 71, 74),  # G
        (69, 73, 76),  # A
    ]

    # Create full song structure
    current_bar = 0

    # Intro (accordion and rhythm focused)
    create_intro_section(midi_file, current_bar, base_chords, INTRO_LENGTH)
    current_bar += INTRO_LENGTH

    # First Verse
    create_verse_section(midi_file, current_bar, verse_chords, "first")
    current_bar += VERSE_LENGTH

    # First Chorus
    create_chorus_section(midi_file, current_bar, chorus_chords, "first")
    current_bar += CHORUS_LENGTH

    # Second Verse
    create_verse_section(midi_file, current_bar, verse_chords, "second")
    current_bar += VERSE_LENGTH

    # Second Chorus
    create_chorus_section(midi_file, current_bar, chorus_chords, "second")
    current_bar += CHORUS_LENGTH

    # Bridge
    create_bridge_section(midi_file, current_bar, bridge_chords)
    current_bar += BRIDGE_LENGTH

    # Final Chorus
    create_chorus_section(midi_file, current_bar, chorus_chords, "final")
    current_bar += CHORUS_LENGTH

    # Outro
    create_outro_section(midi_file, current_bar, base_chords, OUTRO_LENGTH)

    with open("danseband_full_arrangement_v3.mid", "wb") as output_file:
        midi_file.writeFile(output_file)


def get_initial_volume(track):
    """Get initial volume levels for each track"""
    volumes = {
        0: 85,  # Tenor Sax (moderate)
        1: 90,  # Accordion (prominent)
        2: 100,  # Bass (full)
        3: 85,  # Rhythm Guitar (moderate)
        4: 95,  # Drums (prominent)
        5: 100,  # Lead Vocal (full)
        6: 82,  # Alto Sax (slightly back)
    }
    return volumes.get(track, 100)


def get_pan_position(track):
    """Get stereo positioning for each track (64 is center)"""
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
    """Updated instrument numbers for more authentic dansband sound"""
    instruments = {
        0: 67,  # Tenor Sax
        1: 21,  # Accordion
        2: 34,  # Electric Bass
        3: 25,  # Acoustic Guitar
        4: 0,  # Standard Kit
        5: 54,  # Voice
        6: 66,  # Alto Sax
    }
    return instruments.get(track, 0)


def setup_vocal_controls(midi_file, track):
    """Initialize expression controls for vocal track"""
    midi_file.addControllerEvent(track, 0, 0, 1, 0)  # Modulation
    midi_file.addControllerEvent(track, 0, 0, 7, 100)  # Volume
    midi_file.addControllerEvent(track, 0, 0, 10, 64)  # Pan center
    midi_file.addPitchWheelEvent(track, 0, 0, 8192)  # Center pitch
    midi_file.addControllerEvent(track, 0, 0, 11, 127)  # Expression


def setup_sax_controls(midi_file, track):
    """Initialize expression controls for saxophone"""
    midi_file.addControllerEvent(track, 0, 0, 1, 0)  # Modulation wheel
    midi_file.addControllerEvent(track, 0, 0, 7, 100)  # Volume
    midi_file.addControllerEvent(track, 0, 0, 10, 64)  # Pan center
    midi_file.addPitchWheelEvent(track, 0, 0, 8192)  # Center pitch wheel
    midi_file.addControllerEvent(track, 0, 0, 11, 100)  # Expression


def create_intro_section(midi_file, start_bar, chords, length):
    # Simplified arrangement for intro
    for bar in range(length):
        chord_idx = bar % len(chords)

        # Just bass and guitar for first 2 bars
        if bar < 2:
            create_bass_pattern(midi_file, 2, [chords[chord_idx]], bar + start_bar)
            create_rhythm_guitar(midi_file, 3, [chords[chord_idx]], bar + start_bar)
        else:
            # Add full arrangement for latter half
            create_full_bar_arrangement(
                midi_file, [chords[chord_idx]], bar + start_bar, "intro"
            )


def create_verse_section(midi_file, start_bar, chords, verse_type):
    for bar in range(len(chords)):
        create_full_bar_arrangement(
            midi_file, [chords[bar]], bar + start_bar, f"verse_{verse_type}"
        )


def create_chorus_section(midi_file, start_bar, chords, chorus_type):
    # More energetic arrangement for chorus
    for bar in range(len(chords)):
        create_full_bar_arrangement(
            midi_file,
            [chords[bar]],
            bar + start_bar,
            f"chorus_{chorus_type}",
            intensity=1.2,  # Increase velocity for chorus
        )


def create_bridge_section(midi_file, start_bar, chords):
    for bar in range(len(chords)):
        create_full_bar_arrangement(
            midi_file, [chords[bar]], bar + start_bar, "bridge", intensity=1.1
        )


def create_outro_section(midi_file, start_bar, chords, length):
    for bar in range(length):
        chord_idx = bar % len(chords)
        create_full_bar_arrangement(
            midi_file,
            [chords[chord_idx]],
            bar + start_bar,
            "outro",
            intensity=0.9,  # Slightly softer for outro
        )


def create_full_bar_arrangement(midi_file, chords, bar, section_type, intensity=1.0):
    """Creates a full bar arrangement with all instruments"""
    velocity_mult = intensity
    if section_type.startswith("chorus"):
        velocity_mult *= 1.1
    elif section_type == "bridge":
        velocity_mult *= 1.05
    elif section_type == "outro":
        velocity_mult *= max(0.9, 1.0 - (bar * 0.05))  # Gradual fadeout

    # Create patterns for each instrument
    create_bass_pattern(midi_file, 2, chords, bar, velocity_mult)
    create_rhythm_guitar(midi_file, 3, chords, bar, velocity_mult)
    create_drum_pattern(midi_file, 4, bar, section_type, velocity_mult)
    create_accordion_part(midi_file, 1, chords, bar, section_type)

    if section_type != "intro":
        create_vocal_melody(midi_file, 5, chords, bar, section_type)
        create_saxophone_part(midi_file, 0, chords, bar, section_type)  # Tenor sax
        create_saxophone_part(
            midi_file, 6, chords, bar, section_type, is_alto=True
        )  # Alto sax


def create_bass_pattern(midi_file, track, chords, bar, intensity=1.0):
    """Enhanced bass pattern with intensity control"""
    root = chords[0][0] - 24
    third = chords[0][1] - 24
    fifth = chords[0][2] - 24

    # Basic pattern with intensity adjustment
    velocities = {
        0: int(100 * intensity),  # Root note
        0.5: int(85 * intensity),  # Up movement
        1: int(90 * intensity),  # Third
        1.5: int(85 * intensity),  # Up to fifth
        2: int(95 * intensity),  # Back to root
        2.5: int(85 * intensity),  # Walking motion
        3: int(85 * intensity),  # Walking notes
        3.5: int(85 * intensity),  # Walking notes
    }

    # Create the pattern with exact timings
    midi_file.addNote(track, 0, root, bar * 4, 0.5, velocities[0])
    midi_file.addNote(track, 0, root + 7, bar * 4 + 0.5, 0.5, velocities[0.5])
    midi_file.addNote(track, 0, third, bar * 4 + 1, 0.5, velocities[1])
    midi_file.addNote(track, 0, fifth, bar * 4 + 1.5, 0.5, velocities[1.5])
    midi_file.addNote(track, 0, root, bar * 4 + 2, 0.5, velocities[2])
    midi_file.addNote(track, 0, root + 5, bar * 4 + 2.5, 0.5, velocities[2.5])

    # Walking notes to next chord
    midi_file.addNote(track, 0, root + 3, bar * 4 + 3, 0.5, velocities[3])
    midi_file.addNote(track, 0, root + 5, bar * 4 + 3.5, 0.5, velocities[3.5])


def create_accordion_part(midi_file, track, chords, bar, section_type):
    """More characteristic dansband accordion part with counter-melodies"""
    base_velocity = 85

    # Basic chord pattern
    for beat in range(4):
        time = bar * 4 + beat

        if section_type.startswith("verse"):
            # More subtle in verse
            if beat in [0, 2]:
                for note in chords[0]:
                    midi_file.addNote(track, 0, note, time, 1, base_velocity)

        elif section_type.startswith("chorus"):
            # More active in chorus with characteristic runs
            if beat == 0:
                for note in chords[0]:
                    midi_file.addNote(track, 0, note, time, 2, base_velocity)
            elif beat == 2:
                # Add typical accordion run
                run_notes = create_accordion_run(chords[0])
                for i, note in enumerate(run_notes):
                    midi_file.addNote(
                        track, 0, note, time + i * 0.25, 0.25, base_velocity
                    )

    # Add bellows effect with expression control
    steps = 16
    for i in range(steps):
        time = bar * 4 + (i / steps)
        value = 100 + int(math.sin(i * math.pi / 8) * 20)
        midi_file.addControllerEvent(track, 0, time, 11, value)


def create_accordion_run(chord):
    """Creates characteristic dansband accordion runs"""
    root = chord[0]
    third = chord[1]
    fifth = chord[2]
    return [root, third, fifth, third, root + 12, fifth, third, root]


def create_rhythm_guitar(midi_file, track, chords, bar, intensity=1.0):
    """Enhanced rhythm guitar with characteristic dansband 'boom-chick' pattern"""
    # Stronger accent on beats 2 and 4
    base_velocity = int(70 * intensity)
    accent_velocity = int(90 * intensity)

    for beat in range(4):
        time = bar * 4 + beat
        # Root note on beats 1 and 3
        if beat in [0, 2]:
            midi_file.addNote(track, 0, chords[0][0] - 12, time, 0.5, base_velocity)

        # Full chord with accent on beats 2 and 4
        if beat in [1, 3]:
            for note in chords[0]:
                midi_file.addNote(track, 0, note, time, 0.5, accent_velocity)
                midi_file.addNote(track, 0, note, time + 0.5, 0.5, base_velocity - 10)


def create_saxophone_part(midi_file, track, chords, bar, section_type, is_alto=False):
    """Add characteristic saxophone lines"""
    base_velocity = 85 if is_alto else 90
    octave_adjust = 12 if is_alto else 0  # Alto plays an octave higher

    if section_type.startswith("verse"):
        # More subtle backing in verse
        if bar % 2 == 0:
            create_sax_backing_phrase(
                midi_file, track, chords[0], bar, octave_adjust, base_velocity
            )

    elif section_type.startswith("chorus"):
        # More prominent in chorus
        if bar % 2 == 0:
            create_sax_chorus_riff(
                midi_file, track, chords[0], bar, octave_adjust, base_velocity
            )
        else:
            create_sax_backing_phrase(
                midi_file, track, chords[0], bar, octave_adjust, base_velocity - 5
            )

    elif section_type == "bridge":
        # Sustained harmonies in bridge
        create_sax_bridge_part(
            midi_file, track, chords[0], bar, octave_adjust, base_velocity
        )


def create_sax_backing_phrase(midi_file, track, chord, bar, octave_adjust, velocity):
    """Creates background saxophone phrases"""
    root = chord[0] + octave_adjust
    third = chord[1] + octave_adjust
    fifth = chord[2] + octave_adjust

    midi_file.addNote(track, 0, third, bar * 4, 2, velocity)
    midi_file.addNote(track, 0, root, bar * 4 + 2, 1, velocity - 5)
    midi_file.addNote(track, 0, fifth, bar * 4 + 3, 1, velocity - 5)


def create_sax_chorus_riff(midi_file, track, chord, bar, octave_adjust, velocity):
    """Creates characteristic dansband saxophone riffs for chorus"""
    root = chord[0] + octave_adjust
    third = chord[1] + octave_adjust
    fifth = chord[2] + octave_adjust

    riff_notes = [root, third, fifth, third, root + 12, fifth, third, root]
    for i, note in enumerate(riff_notes):
        midi_file.addNote(track, 0, note, bar * 4 + i * 0.5, 0.5, velocity)
        add_sax_vibrato(midi_file, track, bar * 4 + i * 0.5, 0.5)


def create_sax_bridge_part(midi_file, track, chord, bar, octave_adjust, velocity):
    """Creates sustained saxophone harmonies for bridge section"""
    third = chord[1] + octave_adjust
    fifth = chord[2] + octave_adjust

    midi_file.addNote(track, 0, third, bar * 4, 4, velocity)
    add_sax_vibrato(midi_file, track, bar * 4, 4)


def add_sax_vibrato(midi_file, track, start_time, duration):
    """Adds characteristic saxophone vibrato"""
    steps = int(duration * 32)
    vibrato_speed = 6.0  # Hz
    depth = 20

    for i in range(steps):
        time = start_time + (i * duration / steps)
        value = 64 + int(math.sin(2 * math.pi * vibrato_speed * i / steps) * depth)
        midi_file.addControllerEvent(track, 0, time, 1, value)


def create_vocal_melody(midi_file, track, chords, bar, section_type):
    """Enhanced vocal melody with section-specific variations"""
    root = chords[0][0]
    third = chords[0][1]
    fifth = chords[0][2]

    # Different melodic patterns for each section type
    if section_type.startswith("verse"):
        if bar % 2 == 0:  # First bar of phrase
            add_vocal_note_with_vibrato(midi_file, track, bar * 4, root + 12, 2)
            add_vocal_note(midi_file, track, bar * 4 + 2, third + 12, 2)
        else:  # Second bar of phrase
            add_vocal_note_with_vibrato(midi_file, track, bar * 4, fifth + 12, 2)
            add_vocal_note_with_fall(midi_file, track, bar * 4 + 2, root + 12, 2)

    elif section_type.startswith("chorus"):
        # More energetic chorus melody
        if bar % 2 == 0:
            add_vocal_note_with_vibrato(midi_file, track, bar * 4, fifth + 12, 1.5)
            add_vocal_note_with_vibrato(
                midi_file, track, bar * 4 + 1.5, third + 12, 1.5
            )
            add_vocal_note(midi_file, track, bar * 4 + 3, root + 12, 1)
        else:
            add_vocal_note_with_vibrato(midi_file, track, bar * 4, third + 12, 2)
            add_vocal_note_with_fall(midi_file, track, bar * 4 + 2, root + 12, 2)

    elif section_type == "bridge":
        # More sustained notes in bridge
        add_vocal_note_with_vibrato(midi_file, track, bar * 4, fifth + 12, 3)
        add_vocal_note_with_fall(midi_file, track, bar * 4 + 3, third + 12, 1)


def add_vocal_note(midi_file, track, start_time, note, duration, velocity=90):
    """Add basic vocal note"""
    midi_file.addNote(track, 0, note, start_time, duration, velocity)


def add_vocal_note_with_vibrato(midi_file, track, start_time, note, duration):
    """Add note with emotional vibrato"""
    midi_file.addNote(track, 0, note, start_time, duration, 85)

    # Add vibrato
    steps = 32
    for i in range(steps):
        time = start_time + (i * duration / steps)
        value = 64 + int(math.sin(i * math.pi / 4) * 32)
        midi_file.addControllerEvent(track, 0, time, 1, value)


def add_vocal_note_with_fall(midi_file, track, start_time, note, duration):
    """Add note with characteristic falling end"""
    midi_file.addNote(track, 0, note, start_time, duration, 85)

    # Add falling pitch at the end
    fall_start = start_time + duration - 0.2
    steps = 32
    for i in range(steps):
        time = fall_start + (i * 0.2 / steps)
        value = 8192 - int((i / steps) * 2048)  # Gradual fall
        midi_file.addPitchWheelEvent(track, 0, time, value)


def create_drum_pattern(midi_file, track, bar, section_type, intensity=1.0):
    """Enhanced drum pattern with more characteristic dansband feels"""
    kick = 36
    snare = 38
    hihat = 42
    crash = 49
    ride = 51

    # Typical dansband drum pattern with stronger backbeat
    kick_vel = int(100 * intensity)
    snare_vel = int(95 * intensity)  # Stronger backbeat
    hihat_vel = int(75 * intensity)

    # Basic pattern
    midi_file.addNote(track, 9, kick, bar * 4, 1, kick_vel)
    midi_file.addNote(track, 9, kick, bar * 4 + 2, 1, kick_vel - 5)

    # Strong backbeat on 2 and 4
    midi_file.addNote(track, 9, snare, bar * 4 + 1, 1, snare_vel)
    midi_file.addNote(track, 9, snare, bar * 4 + 3, 1, snare_vel)

    # Add fills at phrase endings
    if (bar + 1) % 4 == 0:  # End of 4-bar phrase
        create_dansband_drum_fill(midi_file, track, bar * 4 + 3, intensity)
    else:
        # Regular hi-hat pattern
        for eighth in range(8):
            vel = hihat_vel - (5 if eighth % 2 == 0 else 15)
            midi_file.addNote(track, 9, hihat, bar * 4 + eighth * 0.5, 0.5, vel)


def create_dansband_drum_fill(midi_file, track, start_time, intensity):
    """Creates characteristic dansband drum fills"""
    toms = [45, 47, 50]  # Low, mid, high toms
    snare = 38
    crash = 49

    # Simple descending tom fill
    for i, tom in enumerate(reversed(toms)):
        midi_file.addNote(
            track, 9, tom, start_time + i * 0.25, 0.25, int(90 * intensity)
        )

    # End with crash on the 1
    midi_file.addNote(track, 9, crash, start_time + 1, 1, int(100 * intensity))


if __name__ == "__main__":
    create_danseband_template()
