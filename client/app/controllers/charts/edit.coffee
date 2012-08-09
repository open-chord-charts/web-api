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
{User} = require "models/user"


class ChartsEdit extends Spine.Controller
  elements:
    "form": "form"
  events:
    "click form a.btn.cancel": "onCancelButtonClick"
    "change form input, form textarea": "onFormControlChange"
    "submit form": "onFormSubmit"
  logPrefix: "(controllers.charts.edit.ChartsEdit)"
  tag: "article"

  constructor: ->
    super
    @active @onActive

  attachChart: =>
    @chart = Chart.findByAttribute("slug", @slug)
    if @chart
      @chart.updateAttribute("local", true)
      @chart.bind("error", @onChartError)
      @render()

  decorateFormControl: ($element, helpMessage, className) =>
    $element
      .parents(".control-group").removeClass("error warning").addClass(className).end()
      .next(".help-inline").text(helpMessage).end()

  onActive: (params) =>
    Chart.bind("refresh", @onChartRefresh)
    @formModified = false
    @slug = params.slug
    @attachChart()

  onCancelButtonClick: (event) =>
    event.preventDefault()
    if not @formModified or confirm("Forget changes?")
      @navigate("/charts/#{@chart.slug}")

  onChartError: (chart, errors) =>
    for name, text of errors
      @decorateFormControl(@form.find("*[name='#{name}']"), text, "error")

  onChartRefresh: (charts) =>
    @attachChart()

  onFormControlChange: (event) =>
    @formModified = true
    @decorateFormControl($(event.currentTarget), "Modified", "warning")

  onFormSubmit: (event) =>
    event.preventDefault()
    @chart.fromForm(@form).save()
    if @chart.isValid()
      if @formModified
        @chart.updateAttribute("local_dirty", true)
        @chart.ajax().update()
      @navigate("/charts/#{@chart.slug}")

  render: =>
    document.title = "Edit #{@chart.title} – OpenChordCharts.org"
    chart = @chart.attributes()
    @html(require("views/charts/edit")(
      chart: chart
      routes:
        chart: "/charts/#{@chart.slug}"
    ))


module?.exports.ChartsEdit = ChartsEdit
