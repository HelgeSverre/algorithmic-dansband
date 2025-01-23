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


def create_classic_dansband_progression():
    """Creates typical Ole Ivars-style chord progressions"""
    # D major progressions that Ole Ivars commonly use
    # verse_progression = [
    #     [(62, 66, 69), (62, 66, 69)],  # D   D    (2 bars)
    #     [(67, 71, 74), (67, 71, 74)],  # G   G
    #     [(69, 73, 76), (69, 73, 76)],  # A   A
    #     [(62, 66, 69), (62, 66, 69)],  # D   D
    #     [(62, 66, 69), (59, 62, 66)],  # D   Bm
    #     [(67, 71, 74), (69, 73, 76)],  # G   A
    #     [(62, 66, 69), (62, 66, 69)]  # D   D
    # ]
    #
    # chorus_progression = [
    #     [(62, 66, 69), (67, 71, 74)],  # D   G
    #     [(69, 73, 76), (69, 73, 76)],  # A   A
    #     [(67, 71, 74), (67, 71, 74)],  # G   G
    #     [(69, 73, 76), (69, 73, 76)],  # A   A
    #     [(62, 66, 69), (59, 62, 66)],  # D   Bm
    #     [(67, 71, 74), (69, 73, 76)],  # G   A
    #     [(62, 66, 69), (62, 66, 69)]  # D   D
    # ]
    #
    # # Final chorus modulates up half step to E♭
    # final_chorus_progression = [
    #     [(63, 67, 70), (68, 72, 75)],  # E♭  A♭
    #     [(70, 74, 77), (70, 74, 77)],  # B♭  B♭
    #     [(68, 72, 75), (68, 72, 75)],  # A♭  A♭
    #     [(70, 74, 77), (70, 74, 77)],  # B♭  B♭
    #     [(63, 67, 70), (60, 63, 67)],  # E♭  Cm
    #     [(68, 72, 75), (70, 74, 77)],  # A♭  B♭
    #     [(63, 67, 70), (63, 67, 70)]  # E♭  E♭
    # ]

    # verse_progression = [
    #     [(62, 66, 69), (64, 68, 71)],  # D   E7 (secondary dominant to A)
    #     [(69, 73, 76), (67, 71, 74)],  # A   G
    #     [(65, 69, 72), (69, 73, 76)],  # F#7 A  (secondary dominant to Bm)
    #     [(59, 62, 66), (67, 71, 74)],  # Bm  G
    #     [(65, 68, 72), (69, 73, 76)],  # Gm  A7 (minor subdominant for that schlager feel)
    #     [(62, 66, 69), (60, 64, 67)],  # D   Dm (parallel minor borrowed chord)
    #     [(65, 69, 72), (69, 73, 76)]  # F#7 A7 (secondary dominant movement)
    # ]
    #
    # # More dramatic chorus progression
    # chorus_progression = [
    #     [(62, 66, 69), (65, 69, 72)],  # D   F#7
    #     [(59, 62, 66), (63, 67, 70)],  # Bm  Em7
    #     [(67, 71, 74), (65, 68, 72)],  # G   Gm (characteristic minor subdominant)
    #     [(69, 73, 76), (71, 75, 78)],  # A   B7 (secondary dominant)
    #     [(64, 68, 71), (69, 73, 76)],  # E7  A7 (chain of dominants)
    #     [(62, 66, 69), (60, 64, 67)],  # D   Dm (parallel minor for drama)
    #     [(65, 69, 72), (69, 73, 76)]  # F#7 A7 (classic turnaround)
    # ]
    #
    # # Final chorus modulates up half step to E♭ with extra dramatic moves
    # final_chorus_progression = [
    #     [(63, 67, 70), (66, 70, 73)],  # E♭  G7
    #     [(60, 63, 67), (64, 68, 71)],  # Cm  Fm7
    #     [(68, 72, 75), (66, 69, 73)],  # A♭  A♭m
    #     [(70, 74, 77), (72, 76, 79)],  # B♭  C7
    #     [(65, 69, 72), (70, 74, 77)],  # F7  B♭7
    #     [(63, 67, 70), (61, 65, 68)],  # E♭  E♭m
    #     [(66, 70, 73), (70, 74, 77)]  # G7  B♭7
    # ]

    verse_progression = [
        [(67, 71, 74), (67, 71, 74)],  # G   G
        [(72, 76, 79), (72, 76, 79)],  # C   C
        [(74, 78, 81), (74, 78, 81)],  # D   D
        [(67, 71, 74), (67, 71, 74)],  # G   G
        [(67, 71, 74), (64, 67, 71)],  # G   Em
        [(72, 76, 79), (74, 78, 81)],  # C   D
        [(67, 71, 74), (67, 71, 74)],  # G   G
    ]

    # The chorus has that characteristic move to Cm (minor subdominant)
    chorus_progression = [
        [(67, 71, 74), (72, 76, 79)],  # G   C
        [(74, 78, 81), (74, 78, 81)],  # D   D
        [(72, 76, 79), (70, 73, 77)],  # C   Cm  <- This is the characteristic move!
        [(74, 78, 81), (74, 78, 81)],  # D   D
        [(67, 71, 74), (64, 67, 71)],  # G   Em
        [(72, 76, 79), (74, 78, 81)],  # C   D
        [(67, 71, 74), (67, 71, 74)],  # G   G
    ]

    # They often modulate up a step for the final chorus
    final_chorus_progression = [
        [(69, 73, 76), (74, 78, 81)],  # A   D
        [(76, 80, 83), (76, 80, 83)],  # E   E
        [(74, 78, 81), (72, 75, 79)],  # D   Dm
        [(76, 80, 83), (76, 80, 83)],  # E   E
        [(69, 73, 76), (66, 69, 73)],  # A   F#m
        [(74, 78, 81), (76, 80, 83)],  # D   E
        [(69, 73, 76), (69, 73, 76)],  # A   A
    ]

    return verse_progression, chorus_progression, final_chorus_progression


def create_danseband_template():
    # Create MIDI object with 7 tracks
    midi_file = MIDIFile(7, adjust_origin=False, deinterleave=False)

    # Add track names first
    setup_track_names(midi_file)

    # Global settings
    tempo = 126  # Typical Ole Ivars tempo
    time = 0

    # Song structure (in bars)
    INTRO_LENGTH = 8
    VERSE_LENGTH = 14  # 7 progression pairs
    CHORUS_LENGTH = 14
    BRIDGE_LENGTH = 8
    OUTRO_LENGTH = 8

    # Initialize all tracks
    for track in range(7):
        midi_file.addTempo(track, time, tempo)
        midi_file.addControllerEvent(track, 0, 0, 7, get_initial_volume(track))
        midi_file.addControllerEvent(track, 0, 0, 10, get_pan_position(track))
        midi_file.addProgramChange(track, 0, time, get_instrument(track))

    # Get chord progressions
    verse_prog, chorus_prog, final_chorus_prog = create_classic_dansband_progression()

    # Create full song structure
    current_bar = 0

    # Intro
    create_intro_section(midi_file, current_bar, verse_prog[:4], INTRO_LENGTH)
    current_bar += INTRO_LENGTH

    # First Verse
    create_verse_section(midi_file, current_bar, verse_prog, "first")
    current_bar += VERSE_LENGTH

    # First Chorus
    create_chorus_section(midi_file, current_bar, chorus_prog, "first")
    current_bar += CHORUS_LENGTH

    # Second Verse
    create_verse_section(midi_file, current_bar, verse_prog, "second")
    current_bar += VERSE_LENGTH

    # Second Chorus
    create_chorus_section(midi_file, current_bar, chorus_prog, "second")
    current_bar += CHORUS_LENGTH

    # Bridge (using first half of verse progression)
    create_bridge_section(midi_file, current_bar, verse_prog[:4])
    current_bar += BRIDGE_LENGTH

    # Final Chorus (modulated)
    create_chorus_section(midi_file, current_bar, final_chorus_prog, "final")
    current_bar += CHORUS_LENGTH

    # Outro (using last part of final chorus progression)
    create_outro_section(midi_file, current_bar, final_chorus_prog[-4:], OUTRO_LENGTH)

    save_midi_file(midi_file, "danseband_full_arrangement_v3.mid")


def get_initial_volume(track):
    """Get initial volume levels for each track"""
    volumes = {
        0: 85,  # Tenor Sax
        1: 95,  # Accordion (more prominent)
        2: 100,  # Bass
        3: 90,  # Rhythm Guitar
        4: 95,  # Drums
        5: 100,  # Lead Vocal
        6: 82,  # Alto Sax
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
    """Get instrument numbers for each track"""
    instruments = {
        0: 67,  # Tenor Sax
        1: 21,  # Accordion
        2: 34,  # Electric Bass
        3: 25,  # Acoustic Guitar
        4: 0,  # Standard Kit
        5: 53,  # Voice
        6: 66,  # Alto Sax
    }
    return instruments.get(track, 0)


def create_intro_section(midi_file, start_bar, chords, length):
    """Create intro section with gradual instrument entry"""
    for bar in range(length):
        chord_pair = chords[bar // 2 % len(chords)]
        current_chord = chord_pair[bar % 2]
        next_chord = chord_pair[1] if bar % 2 == 0 else chord_pair[0]

        # Start with just rhythm section
        if bar < 4:
            create_rhythm_guitar_ole_ivars(midi_file, 3, current_chord, bar + start_bar)
            create_walking_bass_ole_ivars(
                midi_file, 2, current_chord, next_chord, bar + start_bar
            )
            create_drums_ole_ivars(
                midi_file, 4, bar + start_bar, "intro"
            )  # Added "intro" as section_type
        else:
            # Add full arrangement for latter half
            create_full_bar_arrangement(
                midi_file, current_chord, next_chord, bar + start_bar, "intro"
            )


def create_verse_section(midi_file, start_bar, progression, verse_type):
    """Create verse section with Ole Ivars style arrangement"""
    for bar_pair in range(len(progression)):
        chord_pair = progression[bar_pair]
        for i in range(2):  # Each pair has 2 bars
            current_bar = start_bar + (bar_pair * 2) + i
            current_chord = chord_pair[i]
            next_chord = chord_pair[1] if i == 0 else chord_pair[0]

            create_full_bar_arrangement(
                midi_file, current_chord, next_chord, current_bar, f"verse_{verse_type}"
            )


def create_chorus_section(midi_file, start_bar, progression, chorus_type):
    """Create chorus section with increased intensity"""
    for bar_pair in range(len(progression)):
        chord_pair = progression[bar_pair]
        for i in range(2):
            current_bar = start_bar + (bar_pair * 2) + i
            current_chord = chord_pair[i]
            next_chord = chord_pair[1] if i == 0 else chord_pair[0]

            create_full_bar_arrangement(
                midi_file,
                current_chord,
                next_chord,
                current_bar,
                f"chorus_{chorus_type}",
                intensity=1.2,
            )


def create_bridge_section(midi_file, start_bar, progression):
    """Create bridge section"""
    for bar_pair in range(len(progression)):
        chord_pair = progression[bar_pair]
        for i in range(2):
            current_bar = start_bar + (bar_pair * 2) + i
            current_chord = chord_pair[i]
            next_chord = chord_pair[1] if i == 0 else chord_pair[0]

            create_full_bar_arrangement(
                midi_file,
                current_chord,
                next_chord,
                current_bar,
                "bridge",
                intensity=1.1,
            )


def create_outro_section(midi_file, start_bar, progression, length):
    """Create outro section with gradual fade"""
    for bar_pair in range(len(progression)):
        chord_pair = progression[bar_pair]
        for i in range(2):
            current_bar = start_bar + (bar_pair * 2) + i
            current_chord = chord_pair[i]
            next_chord = chord_pair[1] if i == 0 else chord_pair[0]

            fade_intensity = max(0.5, 1.0 - (bar_pair * 2 + i) / length)
            create_full_bar_arrangement(
                midi_file,
                current_chord,
                next_chord,
                current_bar,
                "outro",
                intensity=fade_intensity,
            )


def create_full_bar_arrangement(
    midi_file, current_chord, next_chord, bar, section_type, intensity=1.0
):
    """Creates a full bar arrangement with all instruments"""
    # Rhythm section
    create_rhythm_guitar_ole_ivars(midi_file, 3, current_chord, bar, intensity)
    create_walking_bass_ole_ivars(midi_file, 2, current_chord, next_chord, bar)
    create_drums_ole_ivars(midi_file, 4, bar, section_type, intensity)

    # Accordion
    create_accordion_ole_ivars(midi_file, 1, current_chord, bar, section_type)

    if section_type != "intro":
        # Melody instruments
        create_vocal_melody_ole_ivars(midi_file, 5, current_chord, bar, section_type)
        create_saxophone_arrangement(
            midi_file, 0, current_chord, bar, section_type
        )  # Tenor
        create_saxophone_arrangement(
            midi_file, 6, current_chord, bar, section_type, is_alto=True
        )  # Alto


def create_rhythm_guitar_ole_ivars(midi_file, track, chord, bar, intensity=1.0):
    """Classic Ole Ivars rhythm guitar pattern"""
    base_velocity = int(75 * intensity)
    accent_velocity = int(95 * intensity)

    # Characteristic boom-chick pattern
    for beat in range(4):
        time = bar * 4 + beat

        # Strong bass note on 1 and 3
        if beat in [0, 2]:
            midi_file.addNote(track, 0, chord[0] - 12, time, 0.45, accent_velocity)

            # Add muted stroke right after
            for note in chord:
                midi_file.addNote(track, 0, note, time + 0.45, 0.05, base_velocity - 20)

        # Upstroke on 2 and 4 with characteristic muting
        if beat in [1, 3]:
            for note in chord:
                midi_file.addNote(track, 0, note, time, 0.4, accent_velocity)
                midi_file.addNote(track, 0, note, time + 0.4, 0.1, base_velocity - 15)


def create_accordion_ole_ivars(midi_file, track, chord, bar, section_type):
    """Classic Ole Ivars accordion style"""
    base_velocity = 90

    # Basic chord pattern with characteristic off-beats
    for beat in range(4):
        time = bar * 4 + beat

        # Main chord hits
        if beat in [0, 2]:
            for note in chord:
                midi_file.addNote(track, 0, note, time, 0.75, base_velocity)

        # Off-beat accents typical of Ole Ivars style
        if beat in [1, 3]:
            for note in chord:
                midi_file.addNote(
                    track, 0, note + 12, time + 0.5, 0.5, base_velocity - 10
                )

    # Add characteristic bellows effect
    steps = 32
    for i in range(steps):
        time = bar * 4 + (i / steps * 4)
        value = 100 + int(math.sin(i * math.pi / 8) * 25)  # Deeper bellows movement
        midi_file.addControllerEvent(track, 0, time, 11, value)


def create_walking_bass_ole_ivars(midi_file, track, chord, next_chord, bar):
    """Classic Ole Ivars walking bass pattern"""
    root = chord[0] - 24
    fifth = chord[2] - 24
    next_root = next_chord[0] - 24 if next_chord else root

    velocities = [100, 85, 90, 85]

    # Basic pattern
    midi_file.addNote(track, 0, root, bar * 4, 1, velocities[0])
    midi_file.addNote(track, 0, fifth, bar * 4 + 1, 1, velocities[1])
    midi_file.addNote(track, 0, root + 7, bar * 4 + 2, 1, velocities[2])

    # Create walking line to next chord
    if next_chord:
        steps = create_walking_steps(root + 7, next_root)
        for i, note in enumerate(steps):
            midi_file.addNote(
                track, 0, note, bar * 4 + 3 + (i * 0.25), 0.25, velocities[3]
            )


def create_walking_steps(start_note, end_note):
    """Creates smooth walking bass lines between chords"""
    if abs(end_note - start_note) <= 3:
        return [start_note, end_note]
    elif end_note > start_note:
        return [start_note, start_note + 2, start_note + 4, end_note]
    else:
        return [start_note, start_note - 2, start_note - 4, end_note]


def create_drums_ole_ivars(midi_file, track, bar, section_type, intensity=1.0):
    """Classic Ole Ivars drum pattern"""
    kick = 36
    snare = 38
    hihat = 42
    crash = 49
    ride = 51

    # Base velocities adjusted for intensity
    kick_vel = int(100 * intensity)
    snare_vel = int(95 * intensity)
    hihat_vel = int(75 * intensity)

    # Basic pattern for all sections
    midi_file.addNote(track, 9, kick, bar * 4, 1, kick_vel)
    midi_file.addNote(track, 9, kick, bar * 4 + 2, 1, kick_vel - 5)

    # Strong backbeat on 2 and 4 (characteristic of Ole Ivars)
    midi_file.addNote(track, 9, snare, bar * 4 + 1, 1, snare_vel)
    midi_file.addNote(track, 9, snare, bar * 4 + 3, 1, snare_vel)

    # Hi-hat pattern varies by section
    if section_type.startswith("chorus"):
        # More energetic hi-hat in chorus
        for eighth in range(8):
            vel = hihat_vel if eighth % 2 == 0 else hihat_vel - 10
            midi_file.addNote(track, 9, hihat, bar * 4 + eighth * 0.5, 0.5, vel)

        # Add crash accents in chorus
        if bar % 4 == 0:  # Every 4 bars
            midi_file.addNote(track, 9, crash, bar * 4, 1, kick_vel)

    elif section_type == "bridge":
        # Ride cymbal in bridge
        for eighth in range(8):
            midi_file.addNote(
                track, 9, ride, bar * 4 + eighth * 0.5, 0.5, hihat_vel - 5
            )

    else:
        # Standard hi-hat pattern
        for eighth in range(8):
            vel = hihat_vel - (5 if eighth % 2 == 0 else 15)
            midi_file.addNote(track, 9, hihat, bar * 4 + eighth * 0.5, 0.5, vel)

    # Add fills at appropriate places
    if (bar + 1) % 4 == 0:  # End of 4-bar phrase
        create_ole_ivars_drum_fill(midi_file, track, bar * 4 + 3, intensity)


def create_ole_ivars_drum_fill(midi_file, track, start_time, intensity):
    """Creates characteristic Ole Ivars style drum fills"""
    toms = [45, 47, 50]  # Low, mid, high toms
    snare = 38
    crash = 49

    fill_velocity = int(90 * intensity)

    # Simple descending tom fill (very characteristic of dansband)
    for i, tom in enumerate(reversed(toms)):
        midi_file.addNote(track, 9, tom, start_time + i * 0.25, 0.25, fill_velocity)

    # End with crash on the 1
    midi_file.addNote(track, 9, crash, start_time + 1, 1, int(100 * intensity))


def create_vocal_melody_ole_ivars(midi_file, track, chord, bar, section_type):
    """Classic Ole Ivars vocal melody from Jag trodde änglarna fanns"""
    base_velocity = 100  # Make vocals more prominent

    if section_type.startswith("verse"):
        # Actual verse melody notes from the song
        # "Jag trodde änglarna fanns bara i himlen..."
        melody_sequence = [
            (74, 1),  # D (quarter note)
            (72, 1),  # C
            (71, 1),  # B
            (69, 1),  # A
            (67, 2),  # G (half note)
            (69, 2),  # A
        ]

        for i, (note, duration) in enumerate(melody_sequence):
            time = bar * 4 + sum(d for _, d in melody_sequence[:i])
            add_vocal_note_with_vibrato(
                midi_file, track, time, note, duration, base_velocity
            )

    elif section_type.startswith("chorus"):
        # Actual chorus melody
        # "För jag har mött dig..."
        melody_sequence = [
            (74, 1),  # D
            (76, 1),  # E
            (77, 2),  # F
            (76, 1),  # E
            (74, 1),  # D
            (72, 2),  # C
        ]

        for i, (note, duration) in enumerate(melody_sequence):
            time = bar * 4 + sum(d for _, d in melody_sequence[:i])
            add_vocal_note_with_vibrato(
                midi_file, track, time, note, duration, base_velocity
            )


def add_vocal_note_with_vibrato(midi_file, track, start_time, note, duration, velocity):
    """Enhanced vibrato for more expressive vocals"""
    midi_file.addNote(track, 0, note, start_time, duration, velocity)

    steps = int(duration * 32)
    vibrato_speed = 5.5  # Slightly slower, more emotional vibrato
    depth = 25  # Deeper vibrato

    # Add slight pitch bend at start (characteristic of Ole Ivars vocals)
    initial_bend_steps = 8
    for i in range(initial_bend_steps):
        time = start_time + (i * 0.1 / initial_bend_steps)
        value = 8192 + int((1.0 - i / initial_bend_steps) * 1024)
        midi_file.addPitchWheelEvent(track, 0, time, value)

    # Add vibrato
    for i in range(steps):
        time = start_time + 0.1 + (i * duration / steps)
        value = 64 + int(math.sin(2 * math.pi * vibrato_speed * i / steps) * depth)
        midi_file.addControllerEvent(track, 0, time, 1, value)


def create_saxophone_arrangement(
    midi_file, track, chord, bar, section_type, is_alto=False
):
    """Create characteristic saxophone parts"""
    base_velocity = 85 if is_alto else 90
    octave = 12 if is_alto else 0

    root = chord[0] + octave
    third = chord[1] + octave
    fifth = chord[2] + octave

    if section_type.startswith("chorus"):
        # More active in chorus
        add_sax_note_with_vibrato(midi_file, track, root, bar * 4, 1, base_velocity)
        add_sax_note_with_vibrato(
            midi_file, track, third, bar * 4 + 1, 1, base_velocity - 5
        )
        add_sax_note_with_vibrato(
            midi_file, track, fifth, bar * 4 + 2, 1, base_velocity - 5
        )
        add_sax_note_with_fall(
            midi_file, track, third, bar * 4 + 3, 1, base_velocity - 10
        )
    else:
        # Background harmonies in verse
        add_sax_note_with_vibrato(
            midi_file, track, third, bar * 4, 2, base_velocity - 10
        )
        add_sax_note_with_vibrato(
            midi_file, track, root, bar * 4 + 2, 2, base_velocity - 15
        )


def add_vocal_note(midi_file, track, note, start_time, duration, velocity):
    """Add basic vocal note"""
    midi_file.addNote(track, 0, note, start_time, duration, velocity)


def add_vocal_note_with_fall(midi_file, track, start_time, note, duration):
    """Add note with characteristic falling end"""
    midi_file.addNote(track, 0, note, start_time, duration, 85)

    fall_start = start_time + duration - 0.2
    steps = 32
    for i in range(steps):
        time = fall_start + (i * 0.2 / steps)
        value = 8192 - int((i / steps) * 2048)
        midi_file.addPitchWheelEvent(track, 0, time, value)


def add_sax_note_with_vibrato(midi_file, track, note, start_time, duration, velocity):
    """Add saxophone note with characteristic vibrato"""
    midi_file.addNote(track, 0, note, start_time, duration, velocity)

    steps = int(duration * 32)
    vibrato_speed = 6.0
    depth = 20

    for i in range(steps):
        time = start_time + (i * duration / steps)
        value = 64 + int(math.sin(2 * math.pi * vibrato_speed * i / steps) * depth)
        midi_file.addControllerEvent(track, 0, time, 1, value)


def add_sax_note_with_fall(midi_file, track, note, start_time, duration, velocity):
    """Add saxophone note with characteristic fall"""
    midi_file.addNote(track, 0, note, start_time, duration, velocity)

    fall_start = start_time + duration - 0.15
    steps = 24
    for i in range(steps):
        time = fall_start + (i * 0.15 / steps)
        value = 8192 - int((i / steps) * 1536)
        midi_file.addPitchWheelEvent(track, 0, time, value)


if __name__ == "__main__":
    create_danseband_template()
