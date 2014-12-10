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


class ApplicationCache extends Spine.Controller
  elements:
    ".container .brand": "brandDiv"

  constructor: (options) ->
    super

    window.applicationCache.oncached = (event) =>
      @log "cached", event
      @brandDiv.text "cached"

    window.applicationCache.onchecking = (event) =>
      @log "checking", event
      @brandDiv.text "checking"

    window.applicationCache.ondownloading = (event) =>
      @log "downloading", event
      @brandDiv.text "downloading"

    window.applicationCache.onerror = (event) =>
      @log "error", event
      @brandDiv.text "error"

    window.applicationCache.onnoupdate = (event) =>
      @log "noupdate", event
      @brandDiv.text "noupdate"

    window.applicationCache.onobsolete = (event) =>
      @log "obsolete", event
      @brandDiv.text "obsolete"

    window.applicationCache.onprogress = (event) =>
      if event.lengthComputable
        percentage = Math.round(event.loaded / event.total * 100) + '%'
        @log "progress #{percentage}", event
        @brandDiv.text "progress #{percentage}"
      else
        @log "progress", event
        @brandDiv.text "progress"

    window.applicationCache.onupdateready = (event) =>
      window.applicationCache.swapCache()
      @log "updateready", event
      @brandDiv.text "updateready"


global.openchordcharts = global.openchordcharts or {}
global.openchordcharts.ApplicationCache = ApplicationCache
