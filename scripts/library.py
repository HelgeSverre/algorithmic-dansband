from midiutil.MidiFile import MIDIFile
import math


class DansebandSong:
    def __init__(self, name="danseband_song", tempo=116):
        self.name = name
        self.tempo = tempo
        self.midi_file = None
        self.current_bar = 0

        # Default song structure
        self.structure = {"intro": 4, "verse": 8, "chorus": 8, "bridge": 4, "outro": 4}

        # Track configuration is fixed for danseband style
        self.tracks = {
            "steel_guitar": 0,
            "accordion": 1,
            "bass": 2,
            "rhythm_guitar": 3,
            "drums": 4,
            "lead_vocal": 5,
        }

    @staticmethod
    def get_initial_volume(track):
        volumes = {
            0: 90,  # Steel Guitar (slightly back)
            1: 85,  # Accordion (moderate)
            2: 100,  # Bass (full)
            3: 85,  # Rhythm Guitar (moderate)
            4: 95,  # Drums (prominent)
            5: 100,  # Lead Vocal (full)
        }
        return volumes.get(track, 100)

    @staticmethod
    def get_pan_position(track):
        positions = {
            0: 70,  # Steel Guitar (slightly right)
            1: 58,  # Accordion (slightly left)
            2: 64,  # Bass (center)
            3: 54,  # Rhythm Guitar (slightly left)
            4: 64,  # Drums (center)
            5: 64,  # Lead Vocal (center)
        }
        return positions.get(track, 64)

    @staticmethod
    def get_instrument(track):
        instruments = {
            0: 26,  # Steel Guitar (Electric Guitar (jazz))
            1: 22,  # Accordion (Harmonica)
            2: 34,  # Electric Bass (Picked Bass)
            3: 25,  # Acoustic Guitar (steel)
            4: 0,  # Standard Kit
            5: 54,  # Synth Voice
        }
        return instruments.get(track, 0)

    def setup_track_names(self):
        track_names = {
            0: "Steel Guitar",
            1: "Accordion",
            2: "Bass",
            3: "Rhythm Guitar",
            4: "Drums",
            5: "Lead Vocal",
        }
        for track, name in track_names.items():
            self.midi_file.addTrackName(track, 0, name)

    def setup_vocal_controls(self, track):
        self.midi_file.addControllerEvent(track, 0, 0, 1, 0)  # Modulation
        self.midi_file.addControllerEvent(track, 0, 0, 7, 100)  # Volume
        self.midi_file.addControllerEvent(track, 0, 0, 10, 64)  # Pan center
        self.midi_file.addPitchWheelEvent(track, 0, 0, 8192)  # Center pitch
        self.midi_file.addControllerEvent(track, 0, 0, 11, 127)  # Expression

    def setup_steel_guitar_controls(self, track):
        self.midi_file.addControllerEvent(track, 0, 0, 1, 0)  # Modulation wheel
        self.midi_file.addControllerEvent(track, 0, 0, 7, 100)  # Volume
        self.midi_file.addControllerEvent(track, 0, 0, 10, 64)  # Pan center
        self.midi_file.addPitchWheelEvent(track, 0, 0, 8192)  # Center pitch wheel

    def set_structure(self, structure_dict):
        """Set custom song structure"""
        self.structure.update(structure_dict)

    def generate_song(self, progressions, arrangement="default"):
        """Generate full song with given chord progressions"""
        # Initialize MIDI file
        self.midi_file = MIDIFile(
            len(self.tracks), adjust_origin=False, deinterleave=False
        )
        self._setup_tracks()

        # Generate sections based on progressions
        self._generate_default_arrangement(progressions)

        # Save MIDI file
        with open(f"{self.name}.mid", "wb") as output_file:
            self.midi_file.writeFile(output_file)

    def _setup_tracks(self):
        """Initialize all tracks with proper names and settings"""
        self.setup_track_names()

        for track in range(len(self.tracks)):
            self.midi_file.addTempo(track, 0, self.tempo)
            self.midi_file.addControllerEvent(
                track, 0, 0, 7, self.get_initial_volume(track)
            )
            self.midi_file.addControllerEvent(
                track, 0, 0, 10, self.get_pan_position(track)
            )
            self.midi_file.addProgramChange(track, 0, 0, self.get_instrument(track))

        self.setup_vocal_controls(self.tracks["lead_vocal"])
        self.setup_steel_guitar_controls(self.tracks["steel_guitar"])

    def _generate_default_arrangement(self, progressions):
        """Generate standard danseband arrangement"""
        # Intro
        self._add_section("intro", progressions["base"], length=self.structure["intro"])

        # First Verse & Chorus
        self._add_section(
            "verse",
            progressions.get("verse", progressions["base"]),
            length=self.structure["verse"],
            section_type="first",
        )
        self._add_section(
            "chorus",
            progressions.get("chorus", progressions["base"]),
            length=self.structure["chorus"],
            section_type="first",
        )

        # Second Verse & Chorus
        self._add_section(
            "verse",
            progressions.get("verse", progressions["base"]),
            length=self.structure["verse"],
            section_type="second",
        )
        self._add_section(
            "chorus",
            progressions.get("chorus", progressions["base"]),
            length=self.structure["chorus"],
            section_type="second",
        )

        # Bridge
        self._add_section(
            "bridge",
            progressions.get("bridge", progressions["base"]),
            length=self.structure["bridge"],
        )

        # Final Chorus & Outro
        self._add_section(
            "chorus",
            progressions.get("chorus", progressions["base"]),
            length=self.structure["chorus"],
            section_type="final",
        )
        self._add_section("outro", progressions["base"], length=self.structure["outro"])

    def _add_section(self, section_name, chords, length, section_type=None):
        """Add a section to the song"""
        if section_name == "intro":
            self._create_intro_section(self.current_bar, chords, length)
        elif section_name == "verse":
            self._create_verse_section(
                self.current_bar, chords * (length // len(chords)), section_type
            )
        elif section_name == "chorus":
            self._create_chorus_section(
                self.current_bar, chords * (length // len(chords)), section_type
            )
        elif section_name == "bridge":
            self._create_bridge_section(
                self.current_bar, chords * (length // len(chords))
            )
        elif section_name == "outro":
            self._create_outro_section(self.current_bar, chords, length)

        self.current_bar += length

    def _create_intro_section(self, start_bar, chords, length):
        """Create intro section"""
        for bar in range(length):
            chord_idx = bar % len(chords)
            # Just bass and guitar for first 2 bars
            if bar < 2:
                self._create_bass_pattern(2, [chords[chord_idx]], bar + start_bar)
                self._create_rhythm_guitar(3, [chords[chord_idx]], bar + start_bar)
            else:
                # Add full arrangement for latter half
                self._create_full_bar_arrangement(
                    [chords[chord_idx]], bar + start_bar, "intro"
                )

    def _create_verse_section(self, start_bar, chords, verse_type):
        """Create verse section"""
        for bar in range(len(chords)):
            self._create_full_bar_arrangement(
                [chords[bar]], bar + start_bar, f"verse_{verse_type}"
            )

    def _create_chorus_section(self, start_bar, chords, chorus_type):
        """Create chorus section"""
        for bar in range(len(chords)):
            self._create_full_bar_arrangement(
                [chords[bar]], bar + start_bar, f"chorus_{chorus_type}", intensity=1.2
            )

    def _create_bridge_section(self, start_bar, chords):
        """Create bridge section"""
        for bar in range(len(chords)):
            self._create_full_bar_arrangement(
                [chords[bar]], bar + start_bar, "bridge", intensity=1.1
            )

    def _create_outro_section(self, start_bar, chords, length):
        """Create outro section"""
        for bar in range(length):
            chord_idx = bar % len(chords)
            self._create_full_bar_arrangement(
                [chords[chord_idx]], bar + start_bar, "outro", intensity=0.9
            )

    def _create_full_bar_arrangement(self, chords, bar, section_type, intensity=1.0):
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
        self._create_bass_pattern(2, chords, bar, velocity_mult)
        self._create_rhythm_guitar(3, chords, bar, velocity_mult)
        self._create_drum_pattern(4, bar, section_type, velocity_mult)

        # Add section-specific arrangements
        if section_type != "intro":
            self._create_vocal_melody(5, chords, bar, section_type)
            self._create_steel_guitar(0, chords, bar, section_type)
            self._create_accordion(1, chords, bar, velocity_mult)

    def _create_vocal_melody(self, track, chords, bar, section_type):
        """Enhanced vocal melody with section-specific variations"""
        root = chords[0][0]
        third = chords[0][1]
        fifth = chords[0][2]

        if section_type.startswith("verse"):
            if bar % 2 == 0:  # First bar of phrase
                self._add_vocal_note_with_scoop(track, bar * 4, root + 12, 2)
                self._add_vocal_note_with_country_bend(
                    track, bar * 4 + 2, third + 12, 2
                )
            else:  # Second bar of phrase
                self._add_vocal_note_with_vibrato(track, bar * 4, fifth + 12, 2)
                self._add_vocal_note_with_fall(track, bar * 4 + 2, root + 12, 2)

        elif section_type.startswith("chorus"):
            # More energetic chorus melody
            if bar % 2 == 0:
                self._add_vocal_note_with_country_bend(track, bar * 4, fifth + 12, 1.5)
                self._add_vocal_note_with_vibrato(track, bar * 4 + 1.5, third + 12, 1.5)
                self._add_vocal_note_with_scoop(track, bar * 4 + 3, root + 12, 1)
            else:
                self._add_vocal_note_with_country_bend(track, bar * 4, third + 12, 2)
                self._add_vocal_note_with_fall(track, bar * 4 + 2, root + 12, 2)

        elif section_type == "bridge":
            # More sustained notes in bridge
            self._add_vocal_note_with_vibrato(track, bar * 4, fifth + 12, 3)
            self._add_vocal_note_with_fall(track, bar * 4 + 3, third + 12, 1)

    def _add_vocal_note_with_scoop(self, track, start_time, note, duration):
        """Add note with characteristic country "scoop" up"""
        self.midi_file.addNote(track, 0, note, start_time, duration, 90)

        steps = 32
        for i in range(steps):
            time = start_time + (i * 0.1 / steps)
            value = int(8192 + (i / steps) * 2048)  # Gradual bend up
            self.midi_file.addPitchWheelEvent(track, 0, time, value)

        self.midi_file.addPitchWheelEvent(track, 0, start_time + 0.1, 8192)

    def _add_vocal_note_with_country_bend(self, track, start_time, note, duration):
        """Add note with characteristic country vocal bend"""
        self.midi_file.addNote(track, 0, note, start_time, duration, 95)

        steps = 64
        for i in range(steps):
            time = start_time + (i * duration / steps)
            value = 8192 + int(math.sin(i * math.pi / 8) * 1024)
            self.midi_file.addPitchWheelEvent(track, 0, time, value)

    def _add_vocal_note_with_vibrato(self, track, start_time, note, duration):
        """Add note with emotional vibrato"""
        self.midi_file.addNote(track, 0, note, start_time, duration, 85)

        steps = 32
        for i in range(steps):
            time = start_time + (i * duration / steps)
            value = 64 + int(math.sin(i * math.pi / 4) * 32)
            self.midi_file.addControllerEvent(track, 0, time, 1, value)

    def _add_vocal_note_with_fall(self, track, start_time, note, duration):
        """Add note with characteristic falling end"""
        self.midi_file.addNote(track, 0, note, start_time, duration, 85)

        fall_start = start_time + duration - 0.2
        steps = 32
        for i in range(steps):
            time = fall_start + (i * 0.2 / steps)
            value = 8192 - int((i / steps) * 2048)  # Gradual fall
            self.midi_file.addPitchWheelEvent(track, 0, time, value)

    def _create_steel_guitar(self, track, chords, bar, section_type):
        """Enhanced steel guitar part with section-specific variations"""
        root = chords[0][0]
        third = chords[0][1]
        fifth = chords[0][2]

        # Add expression control for better dynamics
        self.midi_file.addControllerEvent(track, 0, bar * 4, 11, 110)  # Expression

        if section_type.startswith("verse"):
            self._add_steel_guitar_phrase(track, bar * 4, root, third, fifth, "verse")
        elif section_type.startswith("chorus"):
            # More expression in chorus
            self.midi_file.addControllerEvent(track, 0, bar * 4, 11, 120)
            self._add_steel_guitar_phrase(track, bar * 4, root, third, fifth, "chorus")
        elif section_type == "bridge":
            # Full expression in bridge
            self.midi_file.addControllerEvent(track, 0, bar * 4, 11, 127)
            self._add_steel_guitar_sustained(track, bar * 4, root, third, fifth)

    def _add_steel_guitar_phrase(
        self, track, start_time, root, third, fifth, section_type
    ):
        """Enhanced steel guitar phrase with section variations"""
        swell_intensity = 1.2 if section_type == "chorus" else 1.0

        for i in range(0, 32):
            volume = int((i / 31) * 127 * swell_intensity)
            self.midi_file.addControllerEvent(track, 0, start_time + i / 32, 7, volume)

        if section_type == "chorus":
            # More active chorus pattern
            self.midi_file.addNote(track, 0, root + 12, start_time, 1, 95)
            self.midi_file.addNote(track, 0, fifth + 12, start_time + 1, 1, 90)
            self.midi_file.addNote(track, 0, third + 12, start_time + 2, 1, 90)
            self.midi_file.addNote(track, 0, root + 12, start_time + 3, 1, 85)
        else:
            # Subtle verse pattern
            self.midi_file.addNote(track, 0, root, start_time, 2, 85)
            self.midi_file.addNote(track, 0, third, start_time + 2, 2, 80)

        self._add_steel_guitar_effects(track, start_time, section_type)

    def _add_steel_guitar_sustained(self, track, start_time, root, third, fifth):
        """Long sustained notes for bridge section"""
        self.midi_file.addNote(track, 0, fifth + 12, start_time, 4, 90)
        self._add_steel_guitar_effects(track, start_time, "bridge")

    def _add_steel_guitar_effects(self, track, start_time, section_type):
        """Section-specific steel guitar effects"""
        vibrato_depth = 48 if section_type == "chorus" else 32
        steps = 64

        for i in range(steps):
            time = start_time + (i * 4 / steps)
            value = 64 + int(math.sin(i * math.pi / 8) * vibrato_depth)
            self.midi_file.addControllerEvent(track, 0, time, 1, value)

    def _generate_pitch_bend_curve(self, start_time, duration):
        """Generate smooth pitch bend curve for steel guitar"""
        points = []
        steps = 32
        for i in range(steps):
            time = start_time + (i * duration / steps)
            if i < steps / 2:
                value = 8192 + int((i / (steps / 2)) * 1024)  # Bend up
            else:
                value = 8192 + int((2 - i / (steps / 2)) * 1024)  # Bend back
            points.append((time, value))
        return points

    def _add_vibrato(self, track, start_time, duration):
        """Add realistic vibrato using sine wave"""
        vibrato_freq = 5  # Hz
        steps = int(duration * 32)  # 32 steps per beat
        for i in range(steps):
            time = start_time + (i * duration / steps)
            value = int(64 + 32 * math.sin(2 * math.pi * vibrato_freq * i / steps))
            self.midi_file.addControllerEvent(track, 0, time, 1, value)

    def _create_bass_pattern(self, track, chords, bar, intensity=1.0):
        """Enhanced bass pattern with intensity control"""
        root = chords[0][0] - 24
        third = chords[0][1] - 24
        fifth = chords[0][2] - 24

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
        self.midi_file.addNote(track, 0, root, bar * 4, 0.5, velocities[0])
        self.midi_file.addNote(track, 0, root + 7, bar * 4 + 0.5, 0.5, velocities[0.5])
        self.midi_file.addNote(track, 0, third, bar * 4 + 1, 0.5, velocities[1])
        self.midi_file.addNote(track, 0, fifth, bar * 4 + 1.5, 0.5, velocities[1.5])
        self.midi_file.addNote(track, 0, root, bar * 4 + 2, 0.5, velocities[2])
        self.midi_file.addNote(track, 0, root + 5, bar * 4 + 2.5, 0.5, velocities[2.5])

        # Walking notes to next chord
        self.midi_file.addNote(track, 0, root + 3, bar * 4 + 3, 0.5, velocities[3])
        self.midi_file.addNote(track, 0, root + 5, bar * 4 + 3.5, 0.5, velocities[3.5])

    def _create_accordion(self, track, chords, bar, intensity=1.0):
        """Enhanced accordion part with better expression"""
        base_velocity = int(85 * intensity)
        secondary_velocity = int(80 * intensity)

        # Add bellows effect with expression control
        steps = 16
        for i in range(steps):
            time = bar * 4 + (i / steps)
            value = 100 + int(math.sin(i * math.pi / 8) * 20)
            self.midi_file.addControllerEvent(track, 0, time, 11, value)

        # Full chord on beat 1
        for note in chords[0]:
            self.midi_file.addNote(track, 0, note, bar * 4, 1.5, base_velocity)

        # Chord on beat 3
        for note in chords[0]:
            self.midi_file.addNote(track, 0, note, bar * 4 + 2, 1.5, secondary_velocity)

    def _create_rhythm_guitar(self, track, chords, bar, intensity=1.0):
        """Enhanced rhythm guitar part with intensity control"""
        base_velocity = int(75 * intensity)
        accent_velocity = int(85 * intensity)

        for beat in range(4):
            for note in chords[0]:
                velocity = accent_velocity if beat in [1, 3] else base_velocity
                self.midi_file.addNote(track, 0, note, bar * 4 + beat, 1, velocity)

    def _create_drum_pattern(self, track, bar, section_type, intensity=1.0):
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
        self.midi_file.addNote(track, 9, kick, bar * 4, 1, kick_vel)
        self.midi_file.addNote(track, 9, kick, bar * 4 + 2, 1, kick_vel - 5)

        self.midi_file.addNote(track, 9, snare, bar * 4 + 1, 1, snare_vel)
        self.midi_file.addNote(track, 9, snare, bar * 4 + 3, 1, snare_vel)

        # Section-specific hi-hat patterns
        if section_type.startswith("chorus"):
            # More energetic hi-hat in chorus
            for eighth in range(8):
                vel = hihat_vel if eighth % 2 == 0 else hihat_vel - 10
                self.midi_file.addNote(
                    track, 9, hihat, bar * 4 + eighth * 0.5, 0.5, vel
                )
            # Add crash on first beat of some chorus bars
            if bar % 2 == 0:
                self.midi_file.addNote(track, 9, crash, bar * 4, 1, kick_vel)

        elif section_type == "bridge":
            # Ride cymbal in bridge
            for eighth in range(8):
                self.midi_file.addNote(
                    track, 9, ride, bar * 4 + eighth * 0.5, 0.5, hihat_vel - 5
                )

        else:  # Verse and other sections
            # Standard hi-hat pattern
            for eighth in range(8):
                vel = hihat_vel - (5 if eighth % 2 == 0 else 15)
                self.midi_file.addNote(
                    track, 9, hihat, bar * 4 + eighth * 0.5, 0.5, vel
                )


# Example usage
if __name__ == "__main__":
    # Define chord progressions in D♭ major
    progressions = {
        "base": [
            (61, 65, 68),  # D♭
            (58, 61, 65),  # B♭m
            (66, 70, 73),  # G♭
            (68, 72, 75),  # A♭
        ],
        "chorus": [
            (61, 65, 68),  # D♭
            (68, 72, 75),  # A♭
            (66, 70, 73),  # G♭
            (68, 72, 75),  # A♭
            (61, 65, 68),  # D♭
            (58, 61, 65),  # B♭m
            (66, 70, 73),  # G♭
            (68, 72, 75),  # A♭
        ],
        "bridge": [
            (56, 60, 63),  # A♭m
            (61, 65, 68),  # D♭
            (66, 70, 73),  # G♭
            (68, 72, 75),  # A♭
        ],
    }

    # Create and configure song
    song = DansebandSong("example_danseband_song")

    # Optional: customize song structure
    song.set_structure({"intro": 4, "verse": 8, "chorus": 8, "bridge": 4, "outro": 4})

    # Generate the song
    song.generate_song(progressions)
