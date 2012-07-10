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


{Chart} = require "models/chart"
{OfflineButton} = require "controllers/offline_button"
transpose = require "lib/transpose"


class ChartsShow extends Spine.Controller
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
  logPrefix: "(controllers.charts.show.ChartsShow)"

  constructor: ->
    super
    @routes
      "/charts/:slug": (params) ->
        @slug = params.slug
        @submitButton.detach()
        Chart.bind "change", @render
        Chart.bind "refresh", @onChartRefresh
#        Chart.fetchLocalOrAjax query: {name: "slug", value: @slug}

  onChartRefresh: (charts, options) =>
    @log "onChartRefresh", charts, options
    @chart = Chart.findByAttribute "slug", @slug
    if @chart
      @offlineButton.release() if @offlineButton
      @offlineButton = new OfflineButton(chart: @chart)
      @actionsDiv.prepend(@offlineButton.$el)
      @render()
    else
      @log "Chart \"#{@slug}\" not found"

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
    @html(@template(partRows: transpose.partsToRows(transpose.decorateChart(@chart.attributes()))))
    window.document.title = "#{@chart.title} (#{@chart.key})"

  template: =>
    require "views/chart"


module?.exports.ChartsShow = ChartsShow
