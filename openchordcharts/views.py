# -*- coding: utf-8 -*-

from pyramid.exceptions import Forbidden, NotFound
from pyramid.view import view_config

from . import model


@view_config(route_name='chart', renderer='/chart.mako')
def chart(request):
    slug = request.matchdict.get('slug')
    if not slug:
        return Forbidden()
    chart = model.Chart.find_one(dict(slug=slug))
    if chart is None:
        return NotFound()
    return dict(
        chart=chart,
        )


@view_config(route_name='charts', renderer='/charts.mako')
def charts(request):
    charts = model.Chart.find().limit(100)
    return dict(
        charts=charts,
        )


@view_config(route_name='index', renderer='/index.mako')
def index(request):
    return dict()
