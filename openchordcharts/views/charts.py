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


from biryani.baseconv import cleanup_line, function, pipe, test_in
from biryani.strings import slugify
from pyramid.exceptions import Forbidden, NotFound
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.view import view_config

from openchordcharts.model.chart import Chart
from openchordcharts.utils import iter_chromatic_keys


@view_config(renderer='/chart.mako', route_name='chart')
def chart(request):
    slug = request.matchdict.get('slug')
    if not slug:
        raise Forbidden()
    if request.GET.get('key'):
        key, error = pipe(
                cleanup_line,
                function(lambda s: s.lower()),
                test_in([key.lower() for key in iter_chromatic_keys()]),
                function(lambda s: s.capitalize()),
                )(request.GET['key'])
        if error is not None:
            raise HTTPBadRequest(detail=error)
    else:
        key = None
    chart = Chart.find_one(dict(slug=slug))
    if chart is None:
        raise NotFound()
    if key is not None and key != chart.key:
        for part_name in chart.parts:
            chart.parts[part_name] = list(chart.iter_chords(key=key, part_name=part_name))
        chart.key = key
    return dict(
        chart=chart,
        )


@view_config(permission='edit', renderer='/chart_edit.mako', route_name='chart.edit')
def chart_edit(request):
    slug = request.matchdict.get('slug')
    if not slug:
        raise Forbidden()
    chart = Chart.find_one(dict(slug=slug))
    if chart is None:
        raise NotFound()
    return dict(
        chart=chart,
        )


@view_config(renderer='jsonp', route_name='chart.json')
def chart_json(request):
    slug = request.matchdict.get('slug')
    if not slug:
        raise Forbidden()
    chart = Chart.find_one(dict(slug=slug))
    if chart is None:
        raise NotFound()
    return chart.to_json()


@view_config(renderer='/charts.mako', route_name='charts')
def charts(request):
    settings = request.registry.settings
    spec = {}
    if request.GET.get('q'):
        q_slug = slugify(request.GET['q'])
        if q_slug:
            spec['keywords'] = Chart.get_search_by_keywords_spec(q_slug.split('-'))
    charts = Chart.find(spec).limit(int(settings['charts.limit']))
    return dict(
        charts=charts,
        )
