# -*- coding: utf-8 -*-


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


from pyramid.exceptions import Forbidden, NotFound
from pyramid.view import view_config

from openchordcharts.model.chart import Chart
from openchordcharts.model.user import User


@view_config(route_name='user', renderer='/user.mako')
def user(request):
    slug = request.matchdict.get('slug')
    if not slug:
        raise Forbidden()
    user = User.find_one(dict(slug=slug))
    if user is None:
        raise NotFound()
    user_charts = Chart.find(dict(user=slug))
    return dict(
        user_charts=user_charts,
        )


@view_config(route_name='users')
def users(request):
    return {}
