# -*- coding: utf-8 -*-

import re

from biryani.strings import slugify
from pyramid.exceptions import Forbidden, NotFound
from pyramid.view import view_config

from openchordcharts import model


@view_config(route_name='chart', renderer='/chart.mako')
def chart(request):
    slug = request.matchdict.get('slug')
    if not slug:
        raise Forbidden()
    chart = model.Chart.find_one(dict(slug=slug))
    if chart is None:
        raise NotFound()
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
