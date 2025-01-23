import os
import random
import time


def get_unique_timestamp():
    """Generate a unique timestamp with random suffix to avoid collisions"""
    return f"{int(time.time())}_{random.randint(1000, 9999)}"


def get_generated_path(filename):
    """
    Get the absolute path to the generated directory and ensure it exists.
    This works regardless of where the script is run from.

    Args:
        filename: The name of the file to be created

    Returns:
        str: The absolute path where the file should be created
    """
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Go up one directory from the scripts folder
    project_root = os.path.dirname(script_dir)

    # Path to the generated directory
    generated_dir = os.path.join(project_root, "generated")

    # Create the generated directory if it doesn't exist
    os.makedirs(generated_dir, exist_ok=True)

    # Return the full path including the filename
    return os.path.join(generated_dir, filename)


# Example usage in each script:
def save_midi_file(midi_file, base_filename):
    """
    Save a MIDI file with a unique timestamp in the generated directory.

    Args:
        midi_file: The MIDIFile object to save
        base_filename: The base name for the file (without timestamp)
    """
    timestamp = get_unique_timestamp()
    filename = f"{timestamp}_{base_filename}"
    filepath = get_generated_path(filename)

    with open(filepath, "wb") as output_file:
        midi_file.writeFile(output_file)
    return filepath
