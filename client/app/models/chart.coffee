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


{OfflineLocal} = require "models/offline_local"
transpose = require "lib/transpose"


class Chart extends Spine.Model
  @configure "Chart", "composers", "genre", "key", "offline", "parts", "slug", "structure", "title"
  @extend OfflineLocal
  @extend Spine.Model.Ajax.Methods
  @url: "/charts.json"

  @fetchLocalOrAjax: (params) =>
    refreshCallbacks = @_callbacks.refresh
    @unbind "refresh"
    @one "refresh", (charts, options) =>
      @_callbacks.refresh = refreshCallbacks
#      found = false
#      if @count()
#        if params.query
#          chart = @findByAttribute params.query.name, params.query.value
#          found = true if chart
#        else
#          found = true
      if @count()
        @trigger "refresh", @all(), localStorage: true
      else
        @fetchAjax params
    @fetch params

  @fetchAjax: (params) ->
    @ajax().fetch(params)

  transpose: (toKey) =>
    if toKey != @key
      for partName, chords of @parts
        @parts[partName] = (transpose.transposeChord(chord, @key, toKey) for chord in chords)
      @key = toKey
    @


module?.exports.Chart = Chart
