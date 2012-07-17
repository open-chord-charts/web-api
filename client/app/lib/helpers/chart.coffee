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


commonChromaticKeys = ['Ab', 'A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G']


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
  chart.parts = parts
  chart


partsToRows = (chart) ->
  newParts = []
  for part in chart.parts
    rows = []
    for chord, index in part.chords by 8
      rows.push(part.chords[index...index + 8])
    newParts.push name: part.name, rows: rows
  chart.parts = newParts
  chart


renderChord = (chord) ->
  renderedChord = chord
  # FIXME This is not semantic, I have to rewrite the font!
  renderedChord = renderedChord.replace "#", "<"
  renderedChord = renderedChord.replace "b", ">"
  renderedChord


module?.exports =
  commonChromaticKeys: commonChromaticKeys
  decorateChart: decorateChart
  partsToRows: partsToRows
