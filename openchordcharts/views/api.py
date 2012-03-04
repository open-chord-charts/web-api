# -*- coding: utf-8 -*-

from pyramid.view import view_config

from openchordcharts import model


@view_config(route_name='charts.json', renderer='jsonp')
def charts_json(request):
    title = request.GET.get('title')
    user = request.GET.get('user')
    spec = {}
    if title:
        spec['title'] = title
    if user:
        spec['user'] = user
    return [chart.to_json() for chart in model.Chart.find(spec)]
