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

{ApplicationCacheInfo} = require "controllers/application_cache_info"
{Chart} = require 'models/chart'
{NavBar} = require 'controllers/navbar'
{NavigatorInfo} = require "controllers/navigator_info"
{Stack} = require "controllers/stack"
{User} = require 'models/user'


class App extends Spine.Controller
  elements:
    "footer p.application-cache-info": "applicationCacheInfoParagraph"
    ".container article": "article"
    ".navbar": "navbarDiv"
    "footer p.navigator-info": "navigatorInfoParagraph"
  logPrefix: "(App)"

  constructor: ->
    super
    new NavBar el: @navbarDiv
    new ApplicationCacheInfo el: @applicationCacheInfoParagraph
    new NavigatorInfo el: @navigatorInfoParagraph
    new Stack el: @article
    Spine.Route.bind "change", (route, path) =>
      @log "Route change: ", route, path
    Spine.Route.setup(history: true)
#    Chart.ajax().fetch()
    Chart.fetchLocalOrAjax()
    @user = User.create(@options.user) if @options.user


module?.exports.App = App
