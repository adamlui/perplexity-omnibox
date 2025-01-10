"""
Script:       remove-json-keys.py
Version:      2023.9.21
Description:  Remove specific key-value pairs from JSON files in a directory.
Author:       Adam Lui
Review:       Hexakleo
URL:          https://github.com/adamlui/python-utils
"""

import os
import re

# Constants
JSON_FOLDER = '_locales'

# UI Initialization
os.system('color')   # Enable color for terminal
print('\033[0;92m')  # Set font color to bright green
TERMINAL_WIDTH = os.get_terminal_size()[0]


def print_trunc(msg):
    """Prints a message truncated to fit within the terminal width."""
    print(msg if len(msg) < TERMINAL_WIDTH else msg[:TERMINAL_WIDTH - 4] + '...')


# Collect keys to remove
keys_to_remove = []
while True:
    key = input("Enter key to remove (or press ENTER if done): ")
    if not key:
        break
    keys_to_remove.append(key)

# Locate JSON directory
print_trunc(f"Searching for {JSON_FOLDER}...")
script_dir = os.path.abspath(os.path.dirname(__file__))
json_dir = None

# Search script directory and parent directories for the JSON folder
for root, dirs, _ in os.walk(script_dir):
    if JSON_FOLDER in dirs:
        json_dir = os.path.join(root, JSON_FOLDER)
        break

if not json_dir:
    parent_dir = os.path.dirname(script_dir)
    while parent_dir and parent_dir != script_dir:
        for root, dirs, _ in os.walk(parent_dir):
            if JSON_FOLDER in dirs:
                json_dir = os.path.join(root, JSON_FOLDER)
                break
        if json_dir:
            break
        parent_dir = os.path.dirname(parent_dir)

if not json_dir:
    print_trunc(f"Unable to locate the {JSON_FOLDER} directory.")
    exit()

print_trunc(f"JSON directory found: {json_dir}\n")

# Process JSON files
keys_removed = []
keys_skipped = []
processed_count = 0

for root, _, files in os.walk(json_dir):
    for filename in files:
        if filename.endswith('.json'):
            file_path = os.path.join(root, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = f.read()

            modified = False
            for key in keys_to_remove:
                re_key = fr'"{re.escape(key)}".*?[,\n]+.*?(?="|$)'
                data, count = re.subn(re_key, '', data)
                if count > 0:
                    keys_removed.append((key, os.path.relpath(file_path, json_dir)))
                    modified = True
                else:
                    keys_skipped.append((key, os.path.relpath(file_path, json_dir)))

            if modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(data)

            processed_count += 1

# Print summaries
if keys_removed:
    print_trunc("\nKeys removed successfully!\n")
    for key, file_path in keys_removed:
        print(f'Removed key "{key}" in {file_path}')
if keys_skipped:
    print_trunc("\nKeys skipped (not found):\n")
    for key, file_path in keys_skipped:
        print(f'Skipped key "{key}" in {file_path}')

print_trunc("\nKey removal process completed!\n")
print(f"Processed JSON Files: {processed_count}")
print(f"Keys Removed: {len(keys_removed)}")
print(f"Keys Skipped: {len(keys_skipped)}")
