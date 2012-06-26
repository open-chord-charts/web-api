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


from biryani.strings import slugify
from formencode.variabledecode import variable_decode
from pyramid.httpexceptions import HTTPBadRequest, HTTPForbidden, HTTPFound, HTTPNotFound

from openchordcharts.conv import chart_to_json_dict, params_to_chart_data, input_to_key
from openchordcharts.model.chart import Chart


def chart(request):
    slug = request.matchdict.get('slug')
    if not slug:
        raise HTTPForbidden()
    if request.GET.get('key'):
        key, error = input_to_key(request.GET['key'])
        if error is not None:
            raise HTTPBadRequest(detail=error)
    else:
        key = None
    chart = Chart.find_one(dict(slug=slug))
    if chart is None:
        raise HTTPNotFound()
    if key is not None and key != chart.key:
        chart.transpose(key)
    return dict(
        chart=chart,
        )


def create(request):
    chart = Chart()
    if request.method == 'POST':
        params = variable_decode(request.POST)
        chart_data, chart_errors = params_to_chart_data(params)
        if chart_errors is None:
            chart.update_from_dict(chart_data)
            chart.save(safe=True)
            return HTTPFound(location=request.route_path('chart', slug=chart.slug))
    else:
        chart_data = dict()
        chart_errors = None
    return dict(
        cancel_url=request.route_path('charts'),
        chart=chart,
        chart_data=chart_data,
        chart_errors=chart_errors or {},
        form_action_url=request.route_path('chart.create'),
        )


def chart_json(request):
    slug = request.matchdict.get('slug')
    if not slug:
        raise HTTPForbidden()
    if request.GET.get('key'):
        key, error = input_to_key(request.GET['key'])
        if error is not None:
            raise HTTPBadRequest(detail=error)
    else:
        key = None
    chart = Chart.find_one(dict(slug=slug))
    if chart is None:
        raise HTTPNotFound()
    if key is not None and key != chart.key:
        chart.transpose(key)
    return chart_to_json_dict(chart)


def charts(request):
    settings = request.registry.settings
    spec = {}
    if request.GET.get('q'):
        q_slug = slugify(request.GET['q'])
        if q_slug:
            spec['keywords'] = Chart.get_search_by_keywords_spec(q_slug.split('-'))
    charts = Chart.find(spec).sort('title').limit(int(settings['charts.limit']))
    return dict(
        charts=charts,
        )


def edit(request):
    slug = request.matchdict.get('slug')
    if not slug:
        raise HTTPForbidden()
    chart = Chart.find_one(dict(slug=slug))
    if chart is None:
        raise HTTPNotFound()
    if request.method == 'POST':
        params = variable_decode(request.POST)
        chart_data, chart_errors = params_to_chart_data(params)
        if chart_errors is None:
            chart.update_from_dict(chart_data)
            chart.save(safe=True)
            return HTTPFound(location=request.route_path('chart', slug=chart.slug))
    else:
        chart_data = chart.to_bson()
        chart_errors = None
    return dict(
        cancel_url=request.route_path('chart', slug=chart.slug),
        chart=chart,
        chart_data=chart_data,
        chart_errors=chart_errors or {},
        form_action_url=request.route_path('chart.edit', slug=chart.slug),
        )
