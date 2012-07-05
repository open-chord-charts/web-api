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


Spine = require "spine"


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
    @chordsDiv.html(window.ecoTemplates.chart(
      partRows: partsToRows(decorateChart(@chart.attributes()))
    ))
    window.document.title = "#{@chart.title} (#{@chart.key})"


module?.exports.Charts = Charts
