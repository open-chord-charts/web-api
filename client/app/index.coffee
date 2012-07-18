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


require "lib/setup"

{Chart} = require 'models/chart'
{NavBar} = require 'controllers/navbar'
{Offline} = require 'controllers/offline'
{Stack} = require "controllers/stack"
{User} = require 'models/user'


class App extends Spine.Controller
  elements:
    "section.container": "section"
    ".navbar": "navbarDiv"
  logPrefix: "(App)"

  constructor: ->
    super
    new NavBar el: @navbarDiv
    new Stack el: @section
    Spine.Route.setup(history: true)
    User.create(@options.user) if @options.user
    Chart.fetch()


class OfflineApp extends Spine.Controller
  elements:
    "article.static": "article"
  logPrefix: "(OfflineApp)"

  constructor: ->
    super
    new Offline el: @article


module?.exports.App = App
module?.exports.OfflineApp = OfflineApp
