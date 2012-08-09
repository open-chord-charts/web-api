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
    ".actions .btn.edit": "editButton"
    ".btn.fetch": "fetchButton"
    ".actions .btn.json": "jsonButton"
    ".properties .key select": "keySelect"
    ".actions .btn.local": "localButton"
    ".btn.send": "sendButton"
  events:
    "click .btn.fetch": "onFetchButtonClick"
    "change .properties .key select": "onKeySelectChange"
    "click .actions .btn.local": "onLocalButtonClick"
    "click .actions .btn.edit": "onNavigateLinkClick"
    "click a.user": "onNavigateLinkClick"
    "click .btn.send": "onSendButtonClick"
  logPrefix: "(controllers.charts.show.ChartsShow)"
  tag: "article"

  constructor: ->
    super
    @active @onActive

  attachChart: =>
    @chart = Chart.findByAttribute("slug", @slug)
    if @chart
      @chart.bind("change", @onChartChange)
      @render()
    else
      @html("Not found")

  onActive: (params) =>
    Chart.bind("refresh", @onChartRefresh)
    @slug = params.slug
    @attachChart()

  onChartChange: (chart) =>
    if @chart and chart.slug is @chart.slug
      @render()
    else
      @attachChart()

  onChartRefresh: (charts) =>
    @attachChart()

  onFetchButtonClick: (event) =>
    @fetchButton.button("fetching")
    @chart.ajax().reload(
      error: (record) =>
        @fetchButton.button("error")
    )

  onKeySelectChange: (event) =>
    @transposedKey = @keySelect.val()
    @render()

  onLocalButtonClick: (event) =>
    event.preventDefault()
    isLocal = not @chart.local
    return if @chart.local_dirty and not confirm("Forget your changes for this chart?")
    @chart.updateAttribute("local", isLocal)
    if not isLocal
      @chart.local = false
      @chart.local_dirty = false
      @chart.ajax().reload()

  onNavigateLinkClick: (event) =>
    event.preventDefault()
    @navigate getLinkPathname(event.currentTarget)

  onSendButtonClick: (event) =>
    @sendButton.button("sending")
    @chart.ajax().update(
      error: (record) =>
        @sendButton.button("error")
      success: (record) =>
        @chart.updateAttribute("local_dirty", false)
    )

  render: =>
    document.title = "#{@chart.title} (#{@chart.key}) – OpenChordCharts.org"
    chart = @chart.attributes()
    if @transposedKey
      chart.parts = @chart.getTransposedParts(@transposedKey)
    chart = chartHelpers.partsToRows(chartHelpers.decorateChart(chart))
    @html(require("views/charts/show")(
      chart: chart
      commonChromaticKeys: chartHelpers.commonChromaticKeys
      routes:
        chart: "/charts/#{@chart.slug}"
        "chart.edit": "/charts/#{@chart.slug}/edit"
        "chart.history": "/charts/#{@chart.slug}/history"
        "chart.json": "/charts/#{@chart.slug}.json"
        login: $(".navbar a.login").attr("href")
      user: User.first()
    ))
    @jsonButton.attr "target", "_blank"
    @keySelect.val(@transposedKey) if @transposedKey
    @localButton.button "toggle" if @chart.local
    @sendButton.addClass "btn-warning" if @chart.local_dirty


module?.exports.ChartsShow = ChartsShow
