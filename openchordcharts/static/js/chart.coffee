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


OfflineLocal =
  extended: ->
    @change @saveLocal
    @fetch @loadLocal

  saveLocal: ->
    window.localStorage[@className] = JSON.stringify (record for cid, record of @records when record.offline)

  loadLocal: ->
    @refresh(window.localStorage[@className] or [], clear: true)


class Chart extends Spine.Model
  @configure "Chart", "key", "offline", "parts", "slug", "structure", "title"
  @extend OfflineLocal

  transpose: (toKey) =>
    if toKey != @key
      for partName, chords of @parts
        @parts[partName] = (transposeChord(chord, @key, toKey) for chord in chords)
      @key = toKey
    @


class OfflineButton extends Spine.Controller
  attributes:
    "data-toggle": "button"
    rel: "popover"
  className: "btn"
  events:
    "click": "onClick"
  logPrefix: "(OfflineButton)"
  tag: "button"

  constructor: (options) ->
    super
    @el.text "Offline"
    if @chart.offline
      @el.button "toggle"
    @el.popover placement: "bottom"
    @render()
    Chart.bind "change", @render

  onClick: (event) =>
    newOfflineValue = not @chart.offline
    if newOfflineValue
      @log "Chart is now offline"
    else
      @log "Chart is now online"
    @chart.updateAttribute "offline", newOfflineValue

  render: =>
    popover = @el.data "popover"
    if @chart.offline
      @log "Set delete offline popover"
      popover.options.content = "You won't be able to access this page while being offline."
      popover.options.title = "Delete offline data"
    else
      @log "Set keep offline popover"
      popover.options.content = "You will be able to access this page while being offline."
      popover.options.title = "Keep data offline"
    @


class Charts extends Spine.Controller
  elements:
    ".actions": "actionsDiv"
    ".actions .btn.delete": "deleteButton"
    ".chords": "chordsDiv"
    ".properties .key select": "keySelect"
    ".properties .key input[type='submit']": "submitButton"
    ".properties .key form": "transposeForm"
  events:
    "click .actions .btn.delete": "onDeleteButtonClicked"
    "change .properties .key select": "onKeySelectChange"
    "submit .properties .key form": "onTransposeFormSubmit"
  logPrefix: "(Charts)"

  constructor: (options) ->
    super
    @submitButton.detach()
    Chart.bind "change", @onChartChange
    Chart.bind "refresh", @onChartRefresh
    Chart.fetch()
    if @chart
      @log "Chart fetched from localStorage"
    else
      @log "Create new chart"
      Chart.create options.chart
    @actionsDiv.prepend(new OfflineButton(chart: @chart).$el)

  onChartChange: (chart, sourceEvent, options) =>
    if sourceEvent == "create"
      @chart = chart
    @render()

  onChartRefresh: (charts, options) =>
    @chart = Chart.findByAttribute "slug", @options.chart.slug
    if @chart
      @render()

  onDeleteButtonClicked: (event) =>
    if not confirm "Delete \"#{@chart.title}\"?"
      event.preventDefault()

  onKeySelectChange: (event) =>
    @transposeForm.trigger "submit"

  onTransposeFormSubmit: (event) =>
    event.preventDefault()
    @chart.transpose(@keySelect.val()).save()

  render: =>
    @keySelect.val @chart.key
    @chordsDiv.html(global.ecoTemplates.chart(
      partRows: partsToRows(decorateChart(@chart.attributes()))
    ))
    window.document.title = "#{@chart.title} (#{@chart.key})"


global.openchordcharts = global.openchordcharts or {}
global.openchordcharts.Charts = Charts
