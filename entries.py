import json

# Define the file path for saving the entries
FILE_PATH = 'positions.txt'

def add_entry(name, x, y, z):
    # Load the existing entries from the file
    entries = load_entries()
    # Add the new entry to the entries dictionary
    entries[name] = (x, y, z)
    # Save the updated entries to the file
    save_entries(entries)

def remove_entry(name):
    # Load the existing entries from the file
    entries = load_entries()
    # Remove the entry with the specified name
    if name in entries:
        del entries[name]
    # Save the updated entries to the file
    save_entries(entries)

def list_entries():
    # Load the existing entries from the file
    entries = load_entries()
    # Print each entry in the format "name: (x, y, z)"
    for name, pos in entries.items():
        print(f"{name}: {pos}")

def get_entry(name):
    # Load the existing entries from the file
    entries = load_entries()
    # Return the entry with the specified name, or None if it doesn't exist
    return entries.get(name)

def load_entries():
    # Try to load the entries from the file, or return an empty dictionary if it doesn't exist
    try:
        with open(FILE_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_entries(entries):
    # Save the entries to the file in JSON format
    with open(FILE_PATH, 'w') as f:
        json.dump(entries, f)
