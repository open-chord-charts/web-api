# -*- coding: utf-8 -*-


# Open Chord Charts -- Database of free chord charts
# By: Christophe Benz <contact@openchordcharts.org>
#
# Copyright (C) 2012-2013 Christophe Benz
# https://gitorious.org/open-chord-charts/
#
# This file is part of Open Chord Charts.
#
# Open Chord Charts is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Open Chord Charts is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""Music theory functions."""


import re


chord_qualities = ['+', '7', '9', 'aug', 'dim', 'm', 'M', 'm7b5']
chord_regex = re.compile('(?P<key>[A-G][b#]?)(?P<quality>.*)')
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
common_chromatic_keys = ['Ab', 'A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G']
diatonic_keys = ['A', 'B', 'C', 'D', 'E', 'F', 'G']


def compute_chromatic_offset(key):
    for key_offset, keys in enumerate(chromatic_keys):
        if key in keys:
            return key_offset
    return None


def compute_diatonic_offset(key):
    return diatonic_keys.index(key)


def compute_transposed_chord(chord, from_key, to_key):
    assert from_key != to_key
    m = chord_regex.match(chord)
    key, quality = m.group('key'), m.group('quality')
    return compute_transposed_key(key, from_key, to_key) + quality


def compute_transposed_key(key, from_key, to_key):
    if from_key == to_key:
        return key
    diatonic_offset_delta = compute_diatonic_offset(to_key[0]) - compute_diatonic_offset(from_key[0])
    chromatic_offset_delta = compute_chromatic_offset(to_key) - compute_chromatic_offset(from_key)
    key_diatonic_offset = compute_diatonic_offset(key[0])
    key_chromatic_offset = compute_chromatic_offset(key)
    transposed_key_diatonic = diatonic_keys[(key_diatonic_offset + diatonic_offset_delta) % len(diatonic_keys)]
    transposed_keys_chromatic = chromatic_keys[(key_chromatic_offset + chromatic_offset_delta) % len(chromatic_keys)]
    if len(transposed_keys_chromatic) == 1:
        return transposed_keys_chromatic[0]
    else:
        for transposed_key_chromatic in transposed_keys_chromatic:
            if transposed_key_chromatic[0] == transposed_key_diatonic:
                return transposed_key_chromatic
    return None
