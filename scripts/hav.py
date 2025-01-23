import math

from midiutil.MidiFile import MIDIFile

from utils import save_midi_file


def create_danseband_template():
    midi_file = MIDIFile(6, adjust_origin=False, deinterleave=False)

    # Global settings
    tempo = 116  # Adjusted to match more closely with Sakarina's style
    time = 0

    for track in range(6):
        midi_file.addTempo(track, time, tempo)
        midi_file.addProgramChange(track, 0, time, get_instrument(track))

    setup_vocal_controls(midi_file, 5)
    setup_steel_guitar_controls(midi_file, 0)

    # Progression in D♭ major (transposed from C)
    # D♭ - B♭m - G♭ - A♭
    chords = [
        (61, 65, 68),  # D♭ major (D♭, F, A♭)
        (58, 61, 65),  # B♭m (B♭, D♭, F)
        (66, 70, 73),  # G♭ major (G♭, B♭, D♭)
        (68, 72, 75),  # A♭ major (A♭, C, E♭)
    ]

    create_vocal_melody(midi_file, 5, chords)
    create_steel_guitar(midi_file, 0, chords)
    create_accordion(midi_file, 1, chords)
    create_bass_pattern(midi_file, 2, chords)
    create_rhythm_guitar(midi_file, 3, chords)
    create_drum_pattern(midi_file, 4)

    save_midi_file(midi_file, "danseband_db_major.mid")


def get_instrument(track):
    instruments = {
        0: 25,  # Steel Guitar
        1: 21,  # Accordion
        2: 33,  # Electric Bass
        3: 24,  # Acoustic Guitar
        4: 0,  # Standard Kit
        5: 53,  # Voice Ooohs (or 54 for Synth Voice)
    }
    return instruments.get(track, 0)


def setup_vocal_controls(midi_file, track):
    # Initialize expression controls for vocal track
    midi_file.addControllerEvent(track, 0, 0, 1, 0)  # Modulation
    midi_file.addControllerEvent(track, 0, 0, 7, 100)  # Volume
    midi_file.addControllerEvent(track, 0, 0, 10, 64)  # Pan center
    midi_file.addPitchWheelEvent(track, 0, 0, 8192)  # Center pitch
    midi_file.addControllerEvent(track, 0, 0, 11, 127)  # Expression


def add_vocal_phrase_1(midi_file, track, start_time, chord):
    # Rising melodic phrase with characteristic country vocal bends
    root, third, fifth = chord

    # Add initial note with slight scoop
    add_vocal_note_with_scoop(midi_file, track, start_time, root + 12, 1)

    # Rising pattern with emotional emphasis
    add_vocal_note_with_vibrato(midi_file, track, start_time + 1, third + 12, 1)
    add_vocal_note_with_country_bend(midi_file, track, start_time + 2, fifth + 12, 2)


def add_vocal_phrase_2(midi_file, track, start_time, chord):
    # Descending emotional phrase
    root, third, fifth = chord

    # Descending pattern with characteristic country breaks
    add_vocal_note_with_country_bend(midi_file, track, start_time, fifth + 12, 1)
    add_vocal_note_with_vibrato(midi_file, track, start_time + 1, third + 12, 1)
    add_vocal_note_with_fall(midi_file, track, start_time + 2, root + 12, 2)


def add_vocal_phrase_3(midi_file, track, start_time, chord):
    # Hook phrase with typical country emphasis
    root, third, fifth = chord

    # Strong emphasis on hook notes
    add_vocal_note_with_country_bend(midi_file, track, start_time, fifth + 12, 1.5)
    add_vocal_note_with_scoop(midi_file, track, start_time + 1.5, third + 12, 1)
    add_vocal_note_with_vibrato(midi_file, track, start_time + 2.5, root + 12, 1.5)


def add_vocal_phrase_4(midi_file, track, start_time, chord):
    # Resolution phrase with characteristic ending
    root, third, fifth = chord

    # Final phrase with emotional resolution
    add_vocal_note_with_country_bend(midi_file, track, start_time, third + 12, 1)
    add_vocal_note_with_vibrato(midi_file, track, start_time + 1, root + 12, 2)
    add_vocal_note_with_fall(midi_file, track, start_time + 3, root + 12, 1)


def add_vocal_note_with_scoop(midi_file, track, start_time, note, duration):
    # Add note with characteristic country "scoop" up
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
    # Add note with characteristic country vocal bend
    midi_file.addNote(track, 0, note, start_time, duration, 95)

    # Add emotional bend
    steps = 64
    for i in range(steps):
        time = start_time + (i * duration / steps)
        # Create slight wavering effect
        value = 8192 + int(math.sin(i * math.pi / 8) * 1024)
        midi_file.addPitchWheelEvent(track, 0, time, value)


def add_vocal_note_with_vibrato(midi_file, track, start_time, note, duration):
    # Add note with emotional vibrato
    midi_file.addNote(track, 0, note, start_time, duration, 85)

    # Add vibrato
    steps = 32
    for i in range(steps):
        time = start_time + (i * duration / steps)
        value = 64 + int(math.sin(i * math.pi / 4) * 32)
        midi_file.addControllerEvent(track, 0, time, 1, value)


def add_vocal_note_with_fall(midi_file, track, start_time, note, duration):
    # Add note with characteristic falling end
    midi_file.addNote(track, 0, note, start_time, duration, 85)

    # Add falling pitch at the end
    fall_start = start_time + duration - 0.2
    steps = 32
    for i in range(steps):
        time = fall_start + (i * 0.2 / steps)
        value = 8192 - int((i / steps) * 2048)  # Gradual fall
        midi_file.addPitchWheelEvent(track, 0, time, value)


def create_bass_pattern(midi_file, track, chords):
    """Enhanced bass pattern with characteristic Nordic danseband movement"""
    for bar in range(4):
        root = chords[bar][0] - 24  # Two octaves down
        third = chords[bar][1] - 24
        fifth = chords[bar][2] - 24

        # Root note with emphasis
        midi_file.addNote(track, 0, root, bar * 4, 0.5, 100)

        # Up movement
        midi_file.addNote(track, 0, root + 7, bar * 4 + 0.5, 0.5, 85)

        # Third with slight accent
        midi_file.addNote(track, 0, third, bar * 4 + 1, 0.5, 90)

        # Up to fifth
        midi_file.addNote(track, 0, fifth, bar * 4 + 1.5, 0.5, 85)

        # Back to root with emphasis
        midi_file.addNote(track, 0, root, bar * 4 + 2, 0.5, 95)

        # Walking motion
        midi_file.addNote(track, 0, root + 5, bar * 4 + 2.5, 0.5, 85)

        # Calculate walking notes to next chord
        next_root = chords[(bar + 1) % 4][0] - 24

        if next_root > root:
            midi_file.addNote(track, 0, root + 3, bar * 4 + 3, 0.5, 85)
            midi_file.addNote(track, 0, root + 5, bar * 4 + 3.5, 0.5, 85)
        else:
            midi_file.addNote(track, 0, root - 2, bar * 4 + 3, 0.5, 85)
            midi_file.addNote(track, 0, root - 4, bar * 4 + 3.5, 0.5, 85)


def create_vocal_melody(midi_file, track, chords):
    # Adapted for D♭ major range
    for bar in range(4):
        root = chords[bar][0]
        third = chords[bar][1]
        fifth = chords[bar][2]

        # More spacious phrasing typical of Nordic danseband
        if bar == 0:
            add_vocal_note_with_scoop(midi_file, track, bar * 4, root + 12, 2)
            add_vocal_note_with_country_bend(
                midi_file, track, bar * 4 + 2, third + 12, 2
            )
        elif bar == 1:
            add_vocal_note_with_vibrato(midi_file, track, bar * 4, fifth + 12, 2)
            add_vocal_note_with_fall(midi_file, track, bar * 4 + 2, root + 12, 2)
        elif bar == 2:
            add_vocal_note_with_country_bend(midi_file, track, bar * 4, third + 12, 3)
            add_vocal_note_with_vibrato(midi_file, track, bar * 4 + 3, root + 12, 1)
        else:
            add_vocal_note_with_scoop(midi_file, track, bar * 4, root + 12, 2)
            add_vocal_note_with_fall(midi_file, track, bar * 4 + 2, root, 2)


def setup_steel_guitar_controls(midi_file, track):
    # Initialize expression controls
    midi_file.addControllerEvent(track, 0, 0, 1, 0)  # Modulation wheel
    midi_file.addControllerEvent(track, 0, 0, 7, 100)  # Volume
    midi_file.addControllerEvent(track, 0, 0, 10, 64)  # Pan center
    midi_file.addPitchWheelEvent(track, 0, 0, 8192)  # Center pitch wheel


def create_steel_guitar(midi_file, track, chords):
    # Enhanced steel guitar part with Nordic flavor
    for bar in range(4):
        root = chords[bar][0]
        third = chords[bar][1]
        fifth = chords[bar][2]

        # More sustained notes with characteristic bends
        add_steel_guitar_phrase(midi_file, track, bar * 4, root, third, fifth)


def add_steel_guitar_phrase(midi_file, track, start_time, root, third, fifth):
    # Volume swell at phrase start
    for i in range(0, 32):
        volume = int((i / 31) * 127)
        midi_file.addControllerEvent(track, 0, start_time + i / 32, 7, volume)

    # Add note with pitch bend
    midi_file.addNote(track, 0, root, start_time, 2, 90)

    # Add characteristic pitch bend
    bend_points = generate_pitch_bend_curve(start_time, 2)
    for time, value in bend_points:
        midi_file.addPitchWheelEvent(track, 0, time, value)

    # Add vibrato using modulation wheel
    add_vibrato(midi_file, track, start_time, 2)

    # Add second note with steel guitar effects
    add_steel_note_with_effects(midi_file, track, start_time + 2, third, 1)

    # Add final note of phrase
    add_steel_note_with_effects(midi_file, track, start_time + 3, fifth, 1)


def generate_pitch_bend_curve(start_time, duration):
    # Generate smooth pitch bend curve
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
    # Add realistic vibrato using sine wave
    vibrato_freq = 5  # Hz
    steps = int(duration * 32)  # 32 steps per beat
    for i in range(steps):
        time = start_time + (i * duration / steps)
        # Generate sine wave vibrato
        value = int(64 + 32 * math.sin(2 * math.pi * vibrato_freq * i / steps))
        midi_file.addControllerEvent(track, 0, time, 1, value)


def add_steel_note_with_effects(midi_file, track, start_time, note, duration):
    # Add a note with steel guitar effects
    midi_file.addNote(track, 0, note, start_time, duration, 85)

    # Add volume swell
    for i in range(0, 16):
        volume = int((i / 15) * 127)
        midi_file.addControllerEvent(track, 0, start_time + i / 16, 7, volume)

    # Add slight pitch bend
    bend_points = generate_pitch_bend_curve(start_time, duration)
    for time, value in bend_points:
        midi_file.addPitchWheelEvent(track, 0, time, value)


def create_accordion(midi_file, track, chords):
    # More prominent accordion part typical in Nordic danseband
    for bar in range(4):
        # Full chord on beat 1
        for note in chords[bar]:
            midi_file.addNote(track, 0, note, bar * 4, 1.5, 85)

        # Brief rest

        # Chord on beat 3
        for note in chords[bar]:
            midi_file.addNote(track, 0, note, bar * 4 + 2, 1.5, 80)


def create_rhythm_guitar(midi_file, track, chords):
    for bar in range(4):
        for beat in range(4):
            for note in chords[bar]:
                velocity = 85 if beat in [1, 3] else 75
                midi_file.addNote(track, 0, note, bar * 4 + beat, 1, velocity)


def create_drum_pattern(midi_file, track):
    kick = 36
    snare = 38
    hihat = 42

    for bar in range(4):
        # Kick pattern
        midi_file.addNote(track, 9, kick, bar * 4, 1, 100)
        midi_file.addNote(track, 9, kick, bar * 4 + 2, 1, 95)

        # Snare on 2 and 4
        midi_file.addNote(track, 9, snare, bar * 4 + 1, 1, 90)
        midi_file.addNote(track, 9, snare, bar * 4 + 3, 1, 90)

        # Hi-hat pattern
        for eighth in range(8):
            velocity = 75 if eighth % 2 == 0 else 65
            midi_file.addNote(track, 9, hihat, bar * 4 + eighth * 0.5, 0.5, velocity)


if __name__ == "__main__":
    create_danseband_template()
