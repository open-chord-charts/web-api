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


class ChartsShow extends Spine.Controller
  elements:
    ".actions": "actionsDiv"
    ".chords": "chordsDiv"
    ".actions .btn.delete": "deleteButton"
    ".actions .btn.edit": "editButton"
    ".actions .btn.json": "jsonButton"
    ".properties .key select": "keySelect"
    ".actions .btn.local": "localButton"
  events:
    "click .actions .btn.delete": "onDeleteButtonClicked"
    "change .properties .key select": "onKeySelectChange"
    "click .actions .btn.local": "onLocalButtonClick"
    "click a.user": "onNavigateLinkClick"
  logPrefix: "(controllers.charts.show.ChartsShow)"
  tag: "article"

  constructor: ->
    super
    @active @onActive

  onActive: (params) =>
    Chart.bind "change", @onChartChange
    Chart.bind "refresh", @onChartRefresh
    @slug = params.slug
    @chart = Chart.findByAttribute "slug", @slug
    if @chart
      @render()
    else
      @log "Chart not found, waiting"

  onChartChange: (chart, type, options) =>
    @render() if chart.id == @chart.id

  onChartRefresh: (charts) =>
    @chart = Chart.findByAttribute "slug", @slug
    if @chart
      @render()
    else
      @log "Chart not found from refresh event (404)"

  onDeleteButtonClicked: (event) =>
    if not confirm "Delete \"#{@chart.title}\"?"
      event.preventDefault()

  onKeySelectChange: (event) =>
    @transposedKey = @keySelect.val()
    @render()

  onLocalButtonClick: (event) =>
    @localButton.data("popover").tip().remove()
    newLocalValue = not @chart.local
    if newLocalValue
      @log "Chart is now stored in localStorage"
    else
      @log "Chart is no more stored in localStorage"
    @chart.updateAttribute "local", newLocalValue, ajax: false

  onNavigateLinkClick: (event) =>
    event.preventDefault()
    @navigate getLinkPathname(event.target)

  render: =>
    chart = @chart.attributes()
    if @transposedKey
      chart.parts = @chart.getTransposedParts(@transposedKey)
    chart = chartHelpers.partsToRows(chartHelpers.decorateChart(chart))
    @html(require("views/charts/show")(
      chart: chart
      commonChromaticKeys: chartHelpers.commonChromaticKeys
      routes:
        chart: "/charts/#{@chart.slug}"
        "chart.delete": "/charts/#{@chart.slug}/delete"
        "chart.edit": "/charts/#{@chart.slug}/edit"
        "chart.history": "/charts/#{@chart.slug}/history"
        "chart.json": "/charts/#{@chart.slug}.json"
        "chart.undelete": "/charts/#{@chart.slug}/undelete"
        login: $(".navbar a.login").attr("href")
      user: User.first()
    ))
    if @transposedKey
      @keySelect.val(@transposedKey)
    @deleteButton.popover placement: "bottom"
    @editButton.popover placement: "bottom"
    @jsonButton.attr "target", "_blank"
    @localButton.button "toggle" if @chart.local
    if @chart.local
      if @chart.obsolete
        localButtonPopoverOptions =
          content: "Local data is obsolete: a new version of this chart is available. Click to update."
          title: "Update local data"
      else
        localButtonPopoverOptions =
          content: "You won't be able to access this page while being offline."
          title: "Delete local data"
    else
      localButtonPopoverOptions =
        content: "You will be able to access this page while being offline."
        title: "Keep local data"
    @localButton.popover $.extend({}, {placement: "bottom"}, localButtonPopoverOptions)
    document.title = "#{@chart.title} (#{@chart.key}) – OpenChordCharts.org"


module?.exports.ChartsShow = ChartsShow
