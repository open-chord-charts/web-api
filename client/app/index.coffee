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


require "es5-shimify"
require "json2ify"
Spine = require "spine"
require "spine/lib/route"

{ApplicationCacheInfo} = require "controllers/application_cache_info"
{ChartsShow} = require "controllers/charts/show"
{NavigatorInfo} = require "controllers/navigator_info"


class App extends Spine.Controller
  elements:
    "footer p.application-cache-info": "applicationCacheInfoParagraph"
    "footer p.navigator-info": "navigatorInfoParagraph"

  constructor: ->
    super
    new ApplicationCacheInfo el: @el.find @applicationCacheInfoParagraph
    new NavigatorInfo el: @el.find @navigatorInfoParagraph
    new ChartsShow el: @el
    Spine.Route.setup history: true


start = ->
    $("*[rel~='external']").attr "target", "_blank"
    new App el: $("body")


module?.exports.start = start
