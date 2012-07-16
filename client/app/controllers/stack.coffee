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


{ChartsList} = require "controllers/charts/list"
{ChartsSearch} = require "controllers/charts/search"
{ChartsShow} = require "controllers/charts/show"
{Index} = require "controllers/index"
{Offline} = require "controllers/offline"


class Stack extends Spine.Stack
  controllers:
    chart: ChartsShow
    charts: ChartsList
    index: Index
    offline: Offline
    search: ChartsSearch
  logPrefix: "(Stack)"
  routes:
    "/": "index"
    "/charts/:slug": "chart"
    "/charts": "charts"
    "/offline": "offline"
    "/search/:q": "search"


module?.exports.Stack = Stack
