# -*- coding: utf-8 -*-

import re


all_keys = [
    ('Ab', 0),
    ('A', 1),
    ('A#', 2),
    ('Bb', 2),
    ('B', 3),
    ('C', 4),
    ('C#', 5),
    ('Db', 5),
    ('D', 6),
    ('D#', 7),
    ('Eb', 7),
    ('E', 8),
    ('F', 9),
    ('F#', 10),
    ('Gb', 10),
    ('G', 11),
    ('G#', 0),
    ]
chord_regex = re.compile('(?P<root>[A-G][b#]?)(?P<quality>.*)')


def get_key_offset(key):
    for current_key, offset in all_keys:
        if current_key == key:
            return offset
    return None


def get_transposed_chord(chord, key_offset_delta):
    m = chord_regex.match(chord)
    return get_transposed_key(m.group('root'), key_offset_delta) + m.group('quality')


def get_transposed_key(key, key_offset_delta):
    key_offset = get_key_offset(key)
    for current_key, offset in all_keys:
        if offset == (key_offset + key_offset_delta) % 12:
            return current_key
    return None
