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


import re

from biryani.baseconv import cleanup_line, function, pipe, test_in
from biryani.strings import slugify
from pyramid.exceptions import Forbidden, NotFound
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.view import view_config

from openchordcharts.model.chart import Chart
from openchordcharts.utils import iter_chromatic_keys


@view_config(route_name='chart', renderer='/chart.mako')
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


@view_config(route_name='charts', renderer='/charts.mako')
def charts(request):
    q = request.GET.get('q')
    spec = {}
    if q:
        q_words = slugify(q).split('-')
        q_words_regexps = [re.compile(u'^{0}'.format(re.escape(word))) for word in q_words]
        spec['keywords'] = {'$all': q_words_regexps}
    charts = Chart.find(spec).limit(100)
    return dict(
        charts=charts,
        )
