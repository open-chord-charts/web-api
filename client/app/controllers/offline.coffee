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


class Offline extends Spine.Controller
  elements:
    ".progress": "progressDiv"
    ".progress .bar": "progressBarDiv"
    ".row.progress-bar": "progressRowDiv"
    ".status": "statusParagraph"
    "button.stop": "stopButton"
  events:
    "click button.stop": "onStopButtonClicked"
  logPrefix: "(Offline)"

  constructor: ->
    super

    # Online/Offline status
    ononline = @onNavigatorOnline
    onoffline = @onNavigatorOffline
    if navigator.onLine
      @onNavigatorOnline()
    else
      @onNavigatorOffline()

    # Application Cache
    @stopButton.hide()
    applicationCache.oncached = (event) =>
      @log "cached", event
      @progressDiv.removeClass "active progress-striped"
      @setStatus "cached"
      @stopButton.hide()
    applicationCache.onchecking = (event) =>
      @log "checking", event
      @progressDiv.addClass "active progress-striped"
      @setStatus "checking"
    applicationCache.ondownloading = (event) =>
      @log "downloading", event
      @setStatus "downloading"
      @stopButton.show()
    applicationCache.onerror = (event) =>
      @log "error", event
      @setStatus "error. You may be offline"
      @progressRowDiv.hide()
      @stopButton.hide()
    applicationCache.onnoupdate = (event) =>
      @log "noupdate", event
      @progressDiv.removeClass "active progress-striped"
      @progressBarDiv.css "width", "100%"
      @setStatus "no update"
      @stopButton.hide()
    applicationCache.onobsolete = (event) =>
      @log "obsolete", event
      @setStatus "obsolete"
      @stopButton.hide()
    applicationCache.onprogress = (event) =>
      if event.lengthComputable
        percentage = Math.round(event.loaded / event.total * 100) + '%'
        @log "progress #{percentage}", event
        @progressBarDiv.css "width", percentage
      else
        @log "progress (length not computable)", event
        @progressBarDiv.css "width", "100%"
    applicationCache.onupdateready = (event) =>
      applicationCache.swapCache()
      @log "updateready", event
      @progressDiv.removeClass "active progress-striped"
      @setStatus "update ready"
      @stopButton.hide()

  onNavigatorOffline: (event) =>
    @log "offline"
    @setStatus "offline"

  onNavigatorOnline: (event) =>
    @log "online"

  onStopButtonClicked: (event) =>
    applicationCache.abort()

  setStatus: (status) =>
    @statusParagraph.text "Status: #{status}"


module?.exports.Offline = Offline
