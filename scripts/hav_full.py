import math

from midiutil.MidiFile import MIDIFile

from utils import save_midi_file


def setup_track_names(midi_file):
    """Setup proper track names for better MIDI organization"""
    track_names = {
        0: "Steel Guitar",
        1: "Accordion",
        2: "Bass",
        3: "Rhythm Guitar",
        4: "Drums",
        5: "Lead Vocal",
    }

    for track, name in track_names.items():
        # Meta event type 3 is for track name
        midi_file.addTrackName(track, 0, name)


def create_danseband_template():
    # Create MIDI object with 6 tracks
    midi_file = MIDIFile(6, adjust_origin=False, deinterleave=False)

    # Add track names first
    setup_track_names(midi_file)

    # Global settings
    tempo = 116
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

    for track in range(6):
        midi_file.addTempo(track, time, tempo)
        # Add track volume (CC7) for better initial mix
        midi_file.addControllerEvent(track, 0, 0, 7, get_initial_volume(track))
        # Add pan positions (CC10) for better stereo image
        midi_file.addControllerEvent(track, 0, 0, 10, get_pan_position(track))
        midi_file.addProgramChange(track, 0, time, get_instrument(track))

    setup_vocal_controls(midi_file, 5)
    setup_steel_guitar_controls(midi_file, 0)

    # Base chord progression in D♭ major
    base_chords = [
        (61, 65, 68),  # D♭ major (D♭, F, A♭)
        (58, 61, 65),  # B♭m (B♭, D♭, F)
        (66, 70, 73),  # G♭ major (G♭, B♭, D♭)
        (68, 72, 75),  # A♭ major (A♭, C, E♭)
    ]

    # Extended chord progressions for different sections
    verse_chords = base_chords * 2  # 8 bars
    chorus_chords = [
        (61, 65, 68),  # D♭
        (68, 72, 75),  # A♭
        (66, 70, 73),  # G♭
        (68, 72, 75),  # A♭
        (61, 65, 68),  # D♭
        (58, 61, 65),  # B♭m
        (66, 70, 73),  # G♭
        (68, 72, 75),  # A♭
    ]
    bridge_chords = [
        (56, 60, 63),  # A♭m
        (61, 65, 68),  # D♭
        (66, 70, 73),  # G♭
        (68, 72, 75),  # A♭
    ]

    # Create full song structure
    current_bar = 0

    # Intro (simplified progression)
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

    save_midi_file(midi_file, "danseband_full_arrangement.mid")


def get_initial_volume(track):
    """Get initial volume levels for each track"""
    volumes = {
        0: 90,  # Steel Guitar (slightly back)
        1: 85,  # Accordion (moderate)
        2: 100,  # Bass (full)
        3: 85,  # Rhythm Guitar (moderate)
        4: 95,  # Drums (prominent)
        5: 100,  # Lead Vocal (full)
    }
    return volumes.get(track, 100)


def get_pan_position(track):
    """Get stereo positioning for each track (64 is center)"""
    positions = {
        0: 70,  # Steel Guitar (slightly right)
        1: 58,  # Accordion (slightly left)
        2: 64,  # Bass (center)
        3: 54,  # Rhythm Guitar (slightly left)
        4: 64,  # Drums (center)
        5: 64,  # Lead Vocal (center)
    }
    return positions.get(track, 64)


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

    # Adjust velocities based on section type and intensity
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

    # Add section-specific arrangements
    if section_type != "intro":
        create_vocal_melody(midi_file, 5, chords, bar, section_type)
        create_steel_guitar(midi_file, 0, chords, bar, section_type)
        create_accordion(midi_file, 1, chords, bar, velocity_mult)


def create_vocal_melody(midi_file, track, chords, bar, section_type):
    """Enhanced vocal melody with section-specific variations"""
    root = chords[0][0]
    third = chords[0][1]
    fifth = chords[0][2]

    # Different melodic patterns for each section type
    if section_type.startswith("verse"):
        if bar % 2 == 0:  # First bar of phrase
            add_vocal_note_with_scoop(midi_file, track, bar * 4, root + 12, 2)
            add_vocal_note_with_country_bend(
                midi_file, track, bar * 4 + 2, third + 12, 2
            )
        else:  # Second bar of phrase
            add_vocal_note_with_vibrato(midi_file, track, bar * 4, fifth + 12, 2)
            add_vocal_note_with_fall(midi_file, track, bar * 4 + 2, root + 12, 2)

    elif section_type.startswith("chorus"):
        # More energetic chorus melody
        if bar % 2 == 0:
            add_vocal_note_with_country_bend(midi_file, track, bar * 4, fifth + 12, 1.5)
            add_vocal_note_with_vibrato(
                midi_file, track, bar * 4 + 1.5, third + 12, 1.5
            )
            add_vocal_note_with_scoop(midi_file, track, bar * 4 + 3, root + 12, 1)
        else:
            add_vocal_note_with_country_bend(midi_file, track, bar * 4, third + 12, 2)
            add_vocal_note_with_fall(midi_file, track, bar * 4 + 2, root + 12, 2)

    elif section_type == "bridge":
        # More sustained notes in bridge
        add_vocal_note_with_vibrato(midi_file, track, bar * 4, fifth + 12, 3)
        add_vocal_note_with_fall(midi_file, track, bar * 4 + 3, third + 12, 1)


def get_instrument(track):
    """Get instrument numbers for each track with more appropriate sounds"""
    instruments = {
        0: 26,  # Steel Guitar (Electric Guitar (jazz) - warmer tone)
        1: 22,  # Accordion (Harmonica - closer to Nordic accordion sound)
        2: 34,  # Electric Bass (Picked Bass - more defined attack)
        3: 25,  # Acoustic Guitar (Acoustic Guitar (steel) - brighter)
        4: 0,  # Standard Kit
        5: 54,  # Synth Voice (warmer than Voice Oohs)
    }
    return instruments.get(track, 0)


def setup_vocal_controls(midi_file, track):
    """Initialize expression controls for vocal track"""
    midi_file.addControllerEvent(track, 0, 0, 1, 0)  # Modulation
    midi_file.addControllerEvent(track, 0, 0, 7, 100)  # Volume
    midi_file.addControllerEvent(track, 0, 0, 10, 64)  # Pan center
    midi_file.addPitchWheelEvent(track, 0, 0, 8192)  # Center pitch
    midi_file.addControllerEvent(track, 0, 0, 11, 127)  # Expression


def setup_steel_guitar_controls(midi_file, track):
    """Initialize expression controls for steel guitar"""
    midi_file.addControllerEvent(track, 0, 0, 1, 0)  # Modulation wheel
    midi_file.addControllerEvent(track, 0, 0, 7, 100)  # Volume
    midi_file.addControllerEvent(track, 0, 0, 10, 64)  # Pan center
    midi_file.addPitchWheelEvent(track, 0, 0, 8192)  # Center pitch wheel


def add_vocal_note_with_scoop(midi_file, track, start_time, note, duration):
    """Add note with characteristic country "scoop" up"""
    midi_file.addNote(track, 0, note, start_time, duration, 90)

    # Add scoop using pitch bend
    steps = 32
    for i in range(steps):
        time = start_time + (i * 0.1 / steps)
        value = int(8192 + (i / steps) * 2048)  # Gradual bend up
        midi_file.addPitchWheelEvent(track, 0, time, value)

    # Return to center pitch
    midi_file.addPitchWheelEvent(track, 0, start_time + 0.1, 8192)


def add_vocal_note_with_country_bend(midi_file, track, start_time, note, duration):
    """Add note with characteristic country vocal bend"""
    midi_file.addNote(track, 0, note, start_time, duration, 95)

    # Add emotional bend
    steps = 64
    for i in range(steps):
        time = start_time + (i * duration / steps)
        # Create slight wavering effect
        value = 8192 + int(math.sin(i * math.pi / 8) * 1024)
        midi_file.addPitchWheelEvent(track, 0, time, value)


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


def generate_pitch_bend_curve(start_time, duration):
    """Generate smooth pitch bend curve for steel guitar"""
    points = []
    steps = 32
    for i in range(steps):
        time = start_time + (i * duration / steps)
        # Create slight pitch bend up and back
        if i < steps / 2:
            value = 8192 + int((i / (steps / 2)) * 1024)  # Bend up
        else:
            value = 8192 + int((2 - i / (steps / 2)) * 1024)  # Bend back
        points.append((time, value))
    return points


def add_vibrato(midi_file, track, start_time, duration):
    """Add realistic vibrato using sine wave"""
    vibrato_freq = 5  # Hz
    steps = int(duration * 32)  # 32 steps per beat
    for i in range(steps):
        time = start_time + (i * duration / steps)
        # Generate sine wave vibrato
        value = int(64 + 32 * math.sin(2 * math.pi * vibrato_freq * i / steps))
        midi_file.addControllerEvent(track, 0, time, 1, value)


def create_steel_guitar(midi_file, track, chords, bar, section_type):
    """Enhanced steel guitar part with section-specific variations"""
    root = chords[0][0]
    third = chords[0][1]
    fifth = chords[0][2]

    # Add expression control for better dynamics
    midi_file.addControllerEvent(track, 0, bar * 4, 11, 110)  # Expression

    if section_type.startswith("verse"):
        # Subtle fills in verse
        add_steel_guitar_phrase(midi_file, track, bar * 4, root, third, fifth, "verse")

    elif section_type.startswith("chorus"):
        # More expression in chorus
        midi_file.addControllerEvent(track, 0, bar * 4, 11, 120)
        add_steel_guitar_phrase(midi_file, track, bar * 4, root, third, fifth, "chorus")

    elif section_type == "bridge":
        # Full expression in bridge
        midi_file.addControllerEvent(track, 0, bar * 4, 11, 127)
        add_steel_guitar_sustained(midi_file, track, bar * 4, root, third, fifth)


def add_steel_guitar_phrase(
    midi_file, track, start_time, root, third, fifth, section_type
):
    """Enhanced steel guitar phrase with section variations"""
    # Volume swell intensity based on section
    swell_intensity = 1.2 if section_type == "chorus" else 1.0

    for i in range(0, 32):
        volume = int((i / 31) * 127 * swell_intensity)
        midi_file.addControllerEvent(track, 0, start_time + i / 32, 7, volume)

    # Section-specific note patterns
    if section_type == "chorus":
        # More active chorus pattern
        midi_file.addNote(track, 0, root + 12, start_time, 1, 95)
        midi_file.addNote(track, 0, fifth + 12, start_time + 1, 1, 90)
        midi_file.addNote(track, 0, third + 12, start_time + 2, 1, 90)
        midi_file.addNote(track, 0, root + 12, start_time + 3, 1, 85)
    else:
        # Subtle verse pattern
        midi_file.addNote(track, 0, root, start_time, 2, 85)
        midi_file.addNote(track, 0, third, start_time + 2, 2, 80)

    # Add characteristic bends
    add_steel_guitar_effects(midi_file, track, start_time, section_type)


def add_steel_guitar_sustained(midi_file, track, start_time, root, third, fifth):
    """Long sustained notes for bridge section"""
    midi_file.addNote(track, 0, fifth + 12, start_time, 4, 90)
    add_steel_guitar_effects(midi_file, track, start_time, "bridge")


def add_steel_guitar_effects(midi_file, track, start_time, section_type):
    """Section-specific steel guitar effects"""
    # Adjust vibrato intensity based on section
    vibrato_depth = 48 if section_type == "chorus" else 32
    steps = 64

    for i in range(steps):
        time = start_time + (i * 4 / steps)
        # More pronounced vibrato in chorus
        value = 64 + int(math.sin(i * math.pi / 8) * vibrato_depth)
        midi_file.addControllerEvent(track, 0, time, 1, value)


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


def create_accordion(midi_file, track, chords, bar, intensity=1.0):
    """Enhanced accordion part with intensity control"""
    # Adjust velocities based on intensity
    base_velocity = int(85 * intensity)
    secondary_velocity = int(80 * intensity)

    # Add bellows effect with expression control
    steps = 16
    for i in range(steps):
        time = bar * 4 + (i / steps)
        value = 100 + int(math.sin(i * math.pi / 8) * 20)
        midi_file.addControllerEvent(track, 0, time, 11, value)

    # Full chord on beat 1
    for note in chords[0]:
        midi_file.addNote(track, 0, note, bar * 4, 1.5, base_velocity)

    # Chord on beat 3
    for note in chords[0]:
        midi_file.addNote(track, 0, note, bar * 4 + 2, 1.5, secondary_velocity)


def create_rhythm_guitar(midi_file, track, chords, bar, intensity=1.0):
    """Enhanced rhythm guitar part with intensity control"""
    base_velocity = int(75 * intensity)
    accent_velocity = int(85 * intensity)

    for beat in range(4):
        for note in chords[0]:
            velocity = accent_velocity if beat in [1, 3] else base_velocity
            midi_file.addNote(track, 0, note, bar * 4 + beat, 1, velocity)


def create_drum_pattern(midi_file, track, bar, section_type, intensity=1.0):
    """Enhanced drum pattern with section-specific variations"""
    kick = 36
    snare = 38
    hihat = 42
    crash = 49
    ride = 51

    # Base velocities adjusted for intensity
    kick_vel = int(100 * intensity)
    snare_vel = int(90 * intensity)
    hihat_vel = int(70 * intensity)

    # Basic pattern present in all sections
    midi_file.addNote(track, 9, kick, bar * 4, 1, kick_vel)
    midi_file.addNote(track, 9, kick, bar * 4 + 2, 1, kick_vel - 5)

    midi_file.addNote(track, 9, snare, bar * 4 + 1, 1, snare_vel)
    midi_file.addNote(track, 9, snare, bar * 4 + 3, 1, snare_vel)

    # Section-specific hi-hat patterns
    if section_type.startswith("chorus"):
        # More energetic hi-hat in chorus
        for eighth in range(8):
            vel = hihat_vel if eighth % 2 == 0 else hihat_vel - 10
            midi_file.addNote(track, 9, hihat, bar * 4 + eighth * 0.5, 0.5, vel)
        # Add crash on first beat of some chorus bars
        if bar % 2 == 0:
            midi_file.addNote(track, 9, crash, bar * 4, 1, kick_vel)

    elif section_type == "bridge":
        # Ride cymbal in bridge
        for eighth in range(8):
            midi_file.addNote(
                track, 9, ride, bar * 4 + eighth * 0.5, 0.5, hihat_vel - 5
            )

    else:  # Verse and other sections
        # Standard hi-hat pattern
        for eighth in range(8):
            vel = hihat_vel - (5 if eighth % 2 == 0 else 15)
            midi_file.addNote(track, 9, hihat, bar * 4 + eighth * 0.5, 0.5, vel)


if __name__ == "__main__":
    create_danseband_template()
