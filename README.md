# Algorithmic Dansband 💃🎶📻

This repo contains various Python scripts that tries to generate "Dansband"-music as MIDI arrangements
programmatically.

(This type of
music: [1](https://www.youtube.com/watch?v=RvZ0MDjIgxo), [2](https://www.youtube.com/watch?v=vzqRKmZiGI0), [3](https://www.youtube.com/watch?v=kY875ESyOvU))

## Why?

It's funky stuff! 🕺🎶

## What does it actually do?

Tries to generate MIDI files with a "Dansband"-feel, the code spits out a MIDI file, all the code in this repo is
AI-Generated using [Claude AI](https://claude.ai/),

## Does it work?

Meh, not really. But it's not completely trash! 🤷‍♂️

## Output:

Some of the generated MIDI files can be found in the `generated` directory.

- [danseband.mid](./generated/danseband.mid)
- [danseband_db_major.mid](./generated/danseband_db_major.mid)
- [danseband_edm_template.mid](./generated/danseband_edm_template.mid)
- [danseband_full_arrangement.mid](./generated/danseband_full_arrangement.mid)
- [danseband_full_arrangement_v3.mid](./generated/danseband_full_arrangement_v3.mid)
- [example_danseband_song.mid](./generated/example_danseband_song.mid)
- [example_song.mid](./generated/example_song.mid)
- [jag_trodde_anglarna_fans_2.mid](./generated/jag_trodde_anglarna_fans_2.mid)
- [jag_trodde_anglarna_vocal.mid](./generated/jag_trodde_anglarna_vocal.mid)
- [ole_ivars_style_arrangement.mid](./generated/ole_ivars_style_arrangement.mid)
- [ole_ivars_style_arrangement_2.mid](./generated/ole_ivars_style_arrangement_2.mid)
- [ole_ivars_style_arrangement_4.mid](./generated/ole_ivars_style_arrangement_4.mid)

## Setup / Installation

```shell
# Setup virtual environment 
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

## Install dependencies
pip install -r requirements.txt

# Format code
pipx run black scripts/

# Run one of the scripts
python scripts/angels.py
python scripts/dansband.py
python scripts/hav.py
python scripts/hav_full.py
python scripts/hav_full_v2.py
python scripts/hav_full_v3.py
python scripts/himmelen.py
python scripts/library.py
python scripts/library_example.py
python scripts/main.py
```