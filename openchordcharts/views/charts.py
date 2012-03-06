# -*- coding: utf-8 -*-

import re

from biryani.baseconv import cleanup_line, function, pipe, test_in
from biryani.strings import slugify
from pyramid.exceptions import Forbidden, NotFound
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.view import view_config

from openchordcharts import model
from openchordcharts.utils import iter_chromatic_keys


@view_config(route_name='chart', renderer='/chart.mako')
def chart(request):
    slug = request.matchdict.get('slug')
    if not slug:
        raise Forbidden()
    key, error = pipe(
            cleanup_line,
            function(lambda s: s.lower()),
            test_in([key.lower() for key in iter_chromatic_keys()]),
            function(lambda s: s.capitalize()),
            )(request.GET.get('key'))
    if error is not None:
        raise HTTPBadRequest(detail=error)
    chart = model.Chart.find_one(dict(slug=slug))
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
    charts = model.Chart.find(spec).limit(100)
    return dict(
        charts=charts,
        )


@view_config(route_name='index', renderer='/index.mako')
def index(request):
    return dict()
