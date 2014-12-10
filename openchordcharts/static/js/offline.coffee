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


global = @


class ApplicationCacheInfo extends Spine.Controller
  logPrefix: "(ApplicationCache)"

  constructor: (options) ->
    super
    window.applicationCache.oncached = (event) =>
      @log "cached", event
      @html "cached"
    window.applicationCache.onchecking = (event) =>
      @log "checking", event
      @html "checking"
    window.applicationCache.ondownloading = (event) =>
      @log "downloading", event
      @html "downloading"
    window.applicationCache.onerror = (event) =>
      @log "error", event
      @html "error"
    window.applicationCache.onnoupdate = (event) =>
      @log "noupdate", event
      @html "noupdate"
    window.applicationCache.onobsolete = (event) =>
      @log "obsolete", event
      @html "obsolete"
    window.applicationCache.onprogress = (event) =>
      if event.lengthComputable
        percentage = Math.round(event.loaded / event.total * 100) + '%'
        @log "progress #{percentage}", event
        @html "progress #{percentage}"
      else
        @log "progress", event
        @html "progress"
    window.applicationCache.onupdateready = (event) =>
      window.applicationCache.swapCache()
      @log "updateready", event
      @html "updateready"


class NavigatorInfo extends Spine.Controller
  logPrefix: "(Navigator)"

  constructor: (options) ->
    super
    window.ononline = @onNavigatorOnline
    window.onoffline = @onNavigatorOffline
    if window.navigator.onLine
      @onNavigatorOnline()
    else
      @onNavigatorOffline()

  onNavigatorOffline: (event) =>
    @log "offline"
    @html "offline"

  onNavigatorOnline: (event) =>
    @log "online"
    @html "online"


global.openchordcharts = global.openchordcharts or {}
global.openchordcharts.ApplicationCacheInfo = ApplicationCacheInfo
global.openchordcharts.NavigatorInfo = NavigatorInfo
