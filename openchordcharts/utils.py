# -*- coding: utf-8 -*-

import re


diatonic_keys = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

chromatic_keys = [
    ['G#', 'Ab'],
    ['A'],
    ['A#', 'Bb'],
    ['B'],
    ['C'],
    ['C#', 'Db'],
    ['D'],
    ['D#', 'Eb'],
    ['E'],
    ['F'],
    ['F#', 'Gb'],
    ['G'],
    ]

common_chromatic_keys = ['Ab', 'A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'F#', 'G']

chord_regex = re.compile('(?P<key>[A-G][b#]?)(?P<quality>.*)')


def get_chromatic_offset(key):
    for key_offset, keys in enumerate(chromatic_keys):
        if key in keys:
            return key_offset
    return None


def get_diatonic_offset(key):
    return diatonic_keys.index(key)


def get_transposed_chord(chord, from_key, to_key):
    if from_key == to_key:
        return chord
    m = chord_regex.match(chord)
    key, quality = m.group('key'), m.group('quality')
    return get_transposed_key(key, from_key, to_key) + quality


def get_transposed_key(key, from_key, to_key):
    if from_key == to_key:
        return key
    diatonic_offset_delta = get_diatonic_offset(to_key[0]) - get_diatonic_offset(from_key[0])
    chromatic_offset_delta = get_chromatic_offset(to_key) - get_chromatic_offset(from_key)
    key_diatonic_offset = get_diatonic_offset(key[0])
    key_chromatic_offset = get_chromatic_offset(key)
    transposed_key_diatonic = diatonic_keys[(key_diatonic_offset + diatonic_offset_delta) % len(diatonic_keys)]
    transposed_keys_chromatic = chromatic_keys[(key_chromatic_offset + chromatic_offset_delta) % len(chromatic_keys)]
    if len(transposed_keys_chromatic) == 1:
        return transposed_keys_chromatic[0]
    else:
        for transposed_key_chromatic in transposed_keys_chromatic:
            if transposed_key_chromatic[0] == transposed_key_diatonic:
                return transposed_key_chromatic
    return None


def iter_chromatic_keys():
    for keys in chromatic_keys:
        for key in keys:
            yield key
