"""
Script:       translate-en-messages.py
Version:      2024.5.14.1
Description:  Translate messages from en/messages.json to other language directories.
Author:       Adam Lui
Review:       Hexakleo
Homepage:     https://github.com/adamlui/python-utils
"""

import os
import json
from sys import stdout
from translate import Translator

# Constants
LOCALES_FOLDER = '_locales'
TARGET_LANGS = [
    'af', 'am', 'ar', 'az', 'be', 'bem', 'bg', 'bn', 'bo', 'bs', 'ca', 'ceb', 
    'cs', 'cy', 'da', 'de', 'dv', 'dz', 'el', 'en', 'en-GB', 'eo', 'es', 'et', 
    'eu', 'fa', 'fi', 'fo', 'fr', 'gd', 'gl', 'gu', 'haw', 'he', 'hi', 'hr', 
    'ht', 'hu', 'hy', 'id', 'is', 'it', 'ja', 'ka', 'kab', 'kk', 'km', 'kn', 
    'ko', 'ku', 'ky', 'la', 'lb', 'lo', 'lt', 'lv', 'mg', 'mi', 'mk', 'ml', 
    'mn', 'ms', 'mt', 'my', 'ne', 'nl', 'no', 'ny', 'pa', 'pap', 'pl', 'ps', 
    'pt', 'ro', 'ru', 'rw', 'sg', 'si', 'sk', 'sl', 'sm', 'sn', 'so', 'sr', 
    'sv', 'sw', 'ta', 'te', 'tg', 'th', 'ti', 'tk', 'tn', 'to', 'tpi', 'tr', 
    'uk', 'ur', 'uz', 'vi', 'xh', 'yi', 'zh', 'zh-CN', 'zh-HK', 'zh-SG', 
    'zh-TW', 'zu'
]

TERMINAL_WIDTH = os.get_terminal_size()[0]


def print_trunc(msg, end='\n'):
    """Prints a truncated message to fit terminal width."""
    print(msg if len(msg) < TERMINAL_WIDTH else msg[:TERMINAL_WIDTH - 4] + '...', end=end)


def overwrite_print(msg):
    """Dynamically overwrites the current line in the terminal."""
    stdout.write('\r' + msg.ljust(TERMINAL_WIDTH)[:TERMINAL_WIDTH])


# Collect keys to ignore
keys_to_ignore = []
while True:
    key = input('Enter key to ignore (or press ENTER if done): ')
    if not key:
        break
    keys_to_ignore.append(key)

# Locate locales directory
print_trunc(f"\nSearching for {LOCALES_FOLDER}...")
script_dir = os.path.abspath(os.path.dirname(__file__))
locales_dir = None

for root, dirs, _ in os.walk(script_dir):
    if LOCALES_FOLDER in dirs:
        locales_dir = os.path.join(root, LOCALES_FOLDER)
        break

if not locales_dir:
    print_trunc(f"Unable to locate the {LOCALES_FOLDER} directory.")
    exit()

print_trunc(f"_locales directory found: {locales_dir}\n")

# Load English messages
msgs_filename = 'messages.json'
en_msgs_path = os.path.join(locales_dir, 'en', msgs_filename)

with open(en_msgs_path, 'r', encoding='utf-8') as en_file:
    en_messages = json.load(en_file)

# Discover and combine languages
output_langs = list(set(TARGET_LANGS))
for root, dirs, _ in os.walk(locales_dir):
    for folder in dirs:
        discovered_lang = folder.replace('_', '-')
        if discovered_lang not in output_langs:
            output_langs.append(discovered_lang)
output_langs.sort()

# Translate messages
langs_translated = []
for lang_code in output_langs:
    if lang_code.startswith('en'):
        continue  # Skip English locales

    folder = lang_code.replace('-', '_')
    folder_path = os.path.join(locales_dir, folder)
    msgs_path = os.path.join(folder_path, msgs_filename)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    messages = {}
    if os.path.exists(msgs_path):
        with open(msgs_path, 'r', encoding='utf-8') as messages_file:
            messages = json.load(messages_file)

    translated_msgs = {}
    for key, value in en_messages.items():
        if key in keys_to_ignore:
            translated_msgs[key] = value
        else:
            try:
                translator = Translator(to_lang=lang_code)
                translated_msg = translator.translate(value['message'])
                translated_msgs[key] = {'message': translated_msg}
            except Exception:
                translated_msgs[key] = value

    with open(msgs_path, 'w', encoding='utf-8') as output_file:
        json.dump(translated_msgs, output_file, ensure_ascii=False, indent=4)

    langs_translated.append(lang_code)

print_trunc("\nTranslation process completed!\n")
print(f"Languages translated: {len(langs_translated)}")
