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


{SelectedLocal} = require "models/selected_local"
transpose = require "lib/transpose"


class Chart extends Spine.Model
  @configure "Chart", "composers", "created_at", "genre", "key", "local", "local_modified_at", "modified_at", "parts",
    "slug", "structure", "title", "user"
  @extend SelectedLocal
  @extend Spine.Model.Ajax.Methods
  @url: "/charts.json"

  @findByKeywords: (keywords) =>
    @select (chart) ->
      chartKeywords = chart.keywords()
      keywords.every (item) -> item in chartKeywords

  fromForm: (form) =>
    super
    @composers = (value.trim() for value in @composers.trim().split(","))
    @structure = (value.trim() for value in @structure.split(""))
    @

  @fromJSON: (records) =>
    objects = super
    return objects if @count() is 0
    dedupedObjects = []
    for object in objects
      originalObject = @findByAttribute "slug", object.slug
      if originalObject
        objectDate = new Date(object.modified_at).getTime()
        originalObjectDate = new Date(originalObject.modified_at).getTime()
        if originalObjectDate <= objectDate
          attributes = {}
          for key, value of object.attributes()
            if not originalObject[key]
              attributes[key] = value
          originalObject.updateAttributes(attributes)
        else
          for key, value of object.attributes()
            if not originalObject[key]?
              originalObject[key] = value
        dedupedObjects.push originalObject
      else
        dedupedObjects.push object
    dedupedObjects

  getTransposedParts: (toKey) =>
    transposedParts = {}
    if toKey != @key
      for partName, chords of @parts
        transposedParts[partName] = (transpose.transposeChord(chord, @key, toKey) for chord in chords)
    transposedParts

  keywords: =>
    @slug.split("-")

  @slugSort: (a, b) ->
    if a.slug > b.slug then 1 else -1

  @updateAllLocal: ->
    @ajax().fetch(
      data:
        slug: (chart.slug for chart in @findAllByAttribute("local", true))
      processData: true
      traditional: true
    )

  validate: =>
    errors = {}
    errors.title = "Empty" if not @title
    if $.isEmptyObject(errors) then false else errors


module?.exports.Chart = Chart
