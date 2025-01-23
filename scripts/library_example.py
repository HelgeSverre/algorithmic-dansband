from library import DansebandSong

if __name__ == "__main__":
    progression = {
        "base": [
            (61, 65, 68),  # D♭
            (58, 61, 65),  # B♭m
            (66, 70, 73),  # G♭
            (68, 72, 75),  # A♭
        ],
    }

    song = DansebandSong(name="example_song.mid", tempo=116)

    song.set_structure({"intro": 4, "verse": 8, "chorus": 8, "bridge": 4, "outro": 4})

    song.generate_song(progression)
