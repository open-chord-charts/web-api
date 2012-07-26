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
{getLinkPathname} = require "lib/javascript"
{User} = require "models/user"


class ChartsList extends Spine.Controller
  elements:
    ".btn.update": "updateButton"
  events:
    "click ul li a": "onChartLinkClick"
    "click .btn.update": "onUpdateButtonClick"
  logPrefix: "(controllers.charts.list.ChartsList)"
  tag: "article"

  constructor: ->
    super
    @active @onActive
    Chart.bind "ajaxError", @onAjaxError
    Chart.bind "change refresh", @render

  onActive: =>
    document.title = "Charts – OpenChordCharts.org"
    @render()

  onAjaxError: (record, xhr, statusText, error) =>
    @updateButton.button("error")

  onChartLinkClick: (event) =>
    event.preventDefault()
    @navigate getLinkPathname(event.currentTarget)

  onUpdateButtonClick: (event) =>
    @updateButton.button("loading")
    Chart.updateAllLocal()

  render: =>
    @html(require("views/charts/list")(
      charts: Chart.all().sort(Chart.slugSort)
      routes:
        "chart.create": "/charts/create"
        login: $(".navbar a.login").attr("href")
      user: User.first()
    ))


module?.exports.ChartsList = ChartsList
