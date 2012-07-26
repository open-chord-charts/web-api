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


class NavBar extends Spine.Controller
  elements:
    "a.charts": "chartsLink"
    "a.my-charts": "myChartsLink"
    "li": "navigationItems"
    "input.search-query": "searchInput"
  events:
    "click a.brand": "onNavigateLinkClick"
    "click a.charts": "onNavigateLinkClick"
    "click a.my-charts": "onNavigateLinkClick"
    "search input.search-query": "onSearchInputSearch"
  logPrefix: "(controllers.navbar.NavBar)"

  constructor: ->
    super
    Spine.Route.bind "change", @onRouteChange

  onNavigateLinkClick: (event) =>
    event.preventDefault()
    @navigate getLinkPathname(event.currentTarget)

  onRouteChange: (route, path) =>
    @navigationItems.removeClass "active"
    if route.path == "/charts"
      @chartsLink.parent("li").addClass("active")
    else if route.path == "/search/:q"
      match = route.route.exec(path)
      @searchInput.val(match[1])

  onSearchInputSearch: (event) =>
    q = event.currentTarget.value.trim()
    return if not q
    @navigate "/search/#{q}"


module?.exports.NavBar = NavBar
