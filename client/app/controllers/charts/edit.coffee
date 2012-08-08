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
chartHelpers = require "lib/helpers/chart"
{getLinkPathname} = require "lib/javascript"
{User} = require "models/user"


class ChartsEdit extends Spine.Controller
  elements:
    "form.edit": "editForm"
  events:
    "change form input, form textarea": "onInputChange"
    "submit form.edit": "onEditFormSubmit"
  logPrefix: "(controllers.charts.edit.ChartsEdit)"
  tag: "article"

  constructor: ->
    super
    @active @onActive

  getChartAttributes: (inputs) =>
    newAttributes = {}
    for input in inputs
      value = input.value
      if input.name is "composers"
        value = (value.trim() for value in value.split(","))
      newAttributes[input.name] = value
    newAttributes

  onActive: (params) =>
    Chart.bind "refresh", @onChartRefresh
    @slug = params.slug
    @chart = Chart.findByAttribute "slug", @slug
    if @chart
      @render()
    else
      @log "Chart not found, waiting"

  onChartRefresh: (charts) =>
    @chart = Chart.findByAttribute "slug", @slug
    if @chart
      @render()
    else
      @log "Chart not found from refresh event (404)"

  onEditFormSubmit: (event) =>
    event.preventDefault()
    newAttributes = @getChartAttributes($(event.currentTarget).serializeArray())
    @chart.updateAttributes(newAttributes)

  onInputChange: (event) =>
    return if window.onbeforeunload
    window.onbeforeunload = (e) ->
      e = e || window.event
      message = "There are unsaved changes!"
      # For IE and Firefox
      if e
        e.returnValue = message
      # For Safari
      message

  render: =>
    chart = @chart.attributes()
    @html(require("views/charts/edit")(
      chart: chart
      routes:
        chart: "/charts/#{@chart.slug}"
    ))
    document.title = "Edit #{@chart.title} – OpenChordCharts.org"


module?.exports.ChartsEdit = ChartsEdit
