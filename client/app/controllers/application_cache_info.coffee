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


class ApplicationCacheInfo extends Spine.Controller
  logPrefix: "(ApplicationCacheInfo)"

  constructor: ->
    super
    applicationCache.oncached = (event) =>
      @log "cached", event
      @html "cached"
    applicationCache.onchecking = (event) =>
      @log "checking", event
      @html "checking"
    applicationCache.ondownloading = (event) =>
      @log "downloading", event
      @html "downloading"
    applicationCache.onerror = (event) =>
      @log "error", event
      @html "error"
    applicationCache.onnoupdate = (event) =>
      @log "noupdate", event
      @html "noupdate"
    applicationCache.onobsolete = (event) =>
      @log "obsolete", event
      @html "obsolete"
    applicationCache.onprogress = (event) =>
      if event.lengthComputable
        percentage = Math.round(event.loaded / event.total * 100) + '%'
        @log "progress #{percentage}", event
        @html "progress #{percentage}"
      else
        @log "progress", event
        @html "progress"
    applicationCache.onupdateready = (event) =>
      applicationCache.swapCache()
      if confirm "New version available. Reload page?"
        location.reload()
      @log "updateready", event
      @html "updateready"


module?.exports.ApplicationCacheInfo = ApplicationCacheInfo
