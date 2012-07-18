# Open Chord Charts -- Database of free chord charts
# By: Christophe Benz <christophe.benz@gmail.com>
#
# Copyright (C) 2012 Christophe Benz
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


chordRegex = /([A-G][b#]?)(.*)/
chromaticKeys = [
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
diatonicKeys = ['A', 'B', 'C', 'D', 'E', 'F', 'G']


getChromaticIndex = (key) ->
  for keys, keyIndex in chromaticKeys
    return keyIndex if key in keys
  throw new Error("Chromatic index not found")


transposeChord = (chord, fromKey, toKey) ->
  return chord if fromKey == toKey
  match = chordRegex.exec chord
  key = match[1]
  quality = match[2]
  return transposeKey(key, fromKey, toKey) + quality


transposeKey = (key, fromKey, toKey) ->
  return key if fromKey == toKey
  diatonicOffsetDelta = diatonicKeys.indexOf(toKey[0]) - diatonicKeys.indexOf(fromKey[0])
  chromaticOffsetDelta = getChromaticIndex(toKey) - getChromaticIndex(fromKey)
  keyDiatonicOffset = diatonicKeys.indexOf(key[0])
  keyChromaticOffset = getChromaticIndex(key)
  transposedKeyDiatonic = diatonicKeys[(keyDiatonicOffset + diatonicOffsetDelta + diatonicKeys.length) %
    diatonicKeys.length]
  transposedKeysChromatic = chromaticKeys[(keyChromaticOffset + chromaticOffsetDelta + chromaticKeys.length) %
    chromaticKeys.length]
  if transposedKeysChromatic.length == 1
    return transposedKeysChromatic[0]
  else
    for transposedKeyChromatic in transposedKeysChromatic
      if transposedKeyChromatic[0] == transposedKeyDiatonic
        return transposedKeyChromatic
  throw new Error("Transposed key not found")


module?.exports =
  transposeChord: transposeChord
