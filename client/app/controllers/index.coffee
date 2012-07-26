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


{getLinkPathname} = require "lib/javascript"


class Index extends Spine.Controller
  elements:
    ".hero-unit a.charts": "chartsLink"
    "a[rel~='external']": "externalLinks"
  events:
    "click .hero-unit a.charts": "onNavigateLinkClick"
  logPrefix: "(controllers.index.Index)"
  tag: "article"

  constructor: ->
    super
    @active @onActive
    @render()

  onActive: =>
    document.title = "OpenChordCharts.org"

  onNavigateLinkClick: (event) =>
    event.preventDefault()
    @navigate getLinkPathname(event.currentTarget)

  render: =>
    @html(require("views/index")(routes: charts: "/charts"))
    @externalLinks.attr "target", "_blank"


module?.exports.Index = Index
