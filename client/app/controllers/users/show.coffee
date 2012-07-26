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
{getLinkPathname} = require "lib/javascript"
{User} = require "models/user"


class UsersShow extends Spine.Controller
  events:
    "click a": "onNavigateLinkClick"
  logPrefix: "(controllers.users.show.UsersShow)"
  tag: "article"

  constructor: ->
    super
    User.bind "change", @onUserChange
    Chart.bind "change refresh", @render
    @active @onActive

  onActive: (params) =>
    @slug = params.slug
    @render()

  onNavigateLinkClick: (event) =>
    event.preventDefault()
    @navigate getLinkPathname(event.currentTarget)

  onUserChange: (user, type, options) =>
    @user = User.first()
    @render()

  render: =>
    return if not @slug
    @html(require("views/users/show")(
      charts: Chart.findAllByAttribute("user", @slug)
      routes:
        charts: "/charts"
        "chart.create": "/charts/create"
      slug: @slug
      user: @user
    ))
    document.title = "#{@slug} profile – OpenChordCharts.org"


module?.exports.UsersShow = UsersShow
