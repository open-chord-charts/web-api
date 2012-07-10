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


class OfflineButton extends Spine.Controller
  attributes:
    "data-toggle": "button"
    rel: "popover"
  className: "btn offline-button"
  events:
    "click": "onClick"
  logPrefix: "(OfflineButton)"
  tag: "button"

  constructor: ->
    super
    @el.text "Offline"
    if @chart.offline
      @el.button "toggle"
    @el.popover placement: "bottom"
    @render()
    Chart.bind "change", @render

  onClick: (event) =>
    newOfflineValue = not @chart.offline
    if newOfflineValue
      @log "Chart is now offline"
    else
      @log "Chart is now online"
    @chart.updateAttribute "offline", newOfflineValue

  render: =>
    popover = @el.data "popover"
    if @chart.offline
      popover.options.content = "You won't be able to access this page while being offline."
      popover.options.title = "Delete offline data"
    else
      popover.options.content = "You will be able to access this page while being offline."
      popover.options.title = "Keep data offline"
    @


module?.exports.OfflineButton = OfflineButton
