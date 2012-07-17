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


import pkg_resources

import eco
from pyramid.httpexceptions import HTTPForbidden, HTTPNotFound

from openchordcharts.conv import chart_to_json_dict, user_to_json_dict
from openchordcharts.model.chart import Chart
from openchordcharts.model.user import User


def user(request):
    slug = request.matchdict.get('slug')
    if not slug:
        raise HTTPForbidden()
    user = User.find_one(dict(slug=slug))
    if user is None:
        raise HTTPNotFound()
    settings = request.registry.settings
    charts = [chart_to_json_dict(chart) for chart in Chart.find(dict(user=slug)).limit(settings['charts.limit'])]
    template_string = pkg_resources.resource_string('openchordcharts', '/templates/eco/users/show.eco')
    eco_template = eco.render(template_string, charts=charts, routes={
        'chart.create': request.route_path('chart.create'),
        'charts': request.route_path('charts'),
        }, slug=slug, user=user_to_json_dict(request.user),
        )
    return dict(
        eco_template=eco_template,
        )
