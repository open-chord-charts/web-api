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
global = @


decorateChart = (chart) ->
  parts = []
  for partName, partIndex in chart.structure
    newPart = name: partName, chords: []
    for chord, chordIndex in chart.parts[partName]
      if chordIndex > 0 and previousChord == chord or chart.structure.indexOf(partName) != partIndex
        newPart.chords.push "—"
      else
        newPart.chords.push(renderChord(chord))
      previousChord = chord
    parts.push newPart
  parts


getChromaticIndex = (key) ->
    for keys, keyIndex in chromaticKeys
      return keyIndex if key in keys
    throw new Error("Chromatic index not found")


partsToRows = (parts) ->
  newParts = []
  for part in parts
    rows = []
    for chord, index in part.chords by 8
      rows.push(part.chords[index...index + 8])
    newParts.push name: part.name, rows: rows
  newParts


renderChord = (chord) ->
  renderedChord = chord
  # FIXME This is not semantic, I have to rewrite the font!
  renderedChord = renderedChord.replace "#", "<"
  renderedChord = renderedChord.replace "b", ">"
  renderedChord


transposeChord = (chord, fromKey, toKey) ->
  return chord if fromKey == toKey
  m = chordRegex.exec chord
  key = m[1]
  quality = m[2]
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


class Chart extends Spine.Model
  @configure "Chart", "key", "parts", "structure"

  transpose: (toKey) =>
    if toKey != @key
      for partName, chords of @parts
        @parts[partName] = (transposeChord(chord, @key, toKey) for chord in chords)
      @key = toKey
    @


class Charts extends Spine.Controller
  elements:
    ".chords": "chordsDiv"
    ".properties .key select": "keySelect"
    ".properties .key form": "transposeForm"

  events:
    "submit .properties .key form": "onTransposeFormSubmit"

  constructor: (options) ->
    super
    Chart.bind "change", @render
    Chart.create options.chart

  onTransposeFormSubmit: (event) =>
    event.preventDefault()
    Chart.first().transpose(@keySelect.val()).save()

  render: (chart) =>
    @chordsDiv.html(global.ecoTemplates.chart(
      partRows: partsToRows(decorateChart(chart.attributes()))
    ))


global.openchordcharts = global.openchordcharts or {}
global.openchordcharts.Charts = Charts
