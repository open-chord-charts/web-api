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
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound

from openchordcharts.conv import params_to_index_data


def cache_manifest(request):
    data, errors = params_to_index_data(request.params)
    if errors is not None:
        raise HTTPBadRequest(detail=errors)
    if data['appcache']:
        request.response.content_type = 'text/cache-manifest'
        return {}
    else:
        raise HTTPNotFound()


def index(request):
    template_string = pkg_resources.resource_string('openchordcharts', '/templates/eco/index.eco')
    eco_template = eco.render(template_string, routes=dict(charts=request.route_path('charts')))
    return dict(
        eco_template=eco_template,
        )
