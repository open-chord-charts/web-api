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
{User} = require "models/user"


# TODO Extend Spine.List (?)
class ChartsList extends Spine.Controller
  elements:
    ".add.btn": "addButton"
    "ul li a": "chartLink"
  events:
    "click ul li a": "onChartLinkClick"
  logPrefix: "(controllers.charts.list.ChartsList)"

  constructor: ->
    super
    @active @onActive
    Chart.bind "refresh change", @render

  onActive: =>
    document.title = "OpenChordCharts.org: charts"

  onChartLinkClick: (event) =>
    event.preventDefault()
    @navigate event.target.pathname

  render: =>
    @html(require("views/charts")(
      charts: Chart.all()
      isLogged: User.count() > 0
      routes:
        "chart.create": "/charts/create"
        "login": $(".navbar a.login").attr("href")
    ))
    @addButton.popover placement: "bottom"


module?.exports.ChartsList = ChartsList
