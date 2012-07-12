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


class NavBar extends Spine.Controller
  elements:
    "a.brand": "brandLink"
    "a.charts": "chartsLink"
    "input.search-query": "searchInput"
  events:
    "click a.brand": "onNavigateLinkClick"
    "click a.charts": "onNavigateLinkClick"
    "change input.search-query": "onSearchInputChange"
  logPrefix: "(NavBar)"

  constructor: ->
    super
    Spine.Route.bind "change", @onRouteChange

  onNavigateLinkClick: (event) =>
    event.preventDefault()
    @navigate event.target.pathname

  onRouteChange: (route, path) =>
    $li = @chartsLink.parent "li"
    if path == "/charts"
      $li.addClass "active"
    else
      $li.removeClass "active"

  onSearchInputChange: (event) =>
    q = event.target.value.trim()
    return if not q
    keywords = (keyword for keyword in q.split(" ") when keyword)
    @log "onSearchInputChange: keywords: #{keywords}"
    @navigate "/charts#q=#{keywords}"
#    Chart.findByKeywords(keywords)


module?.exports.NavBar = NavBar
