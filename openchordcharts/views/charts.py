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

from biryani.strings import slugify
import eco
from formencode.variabledecode import variable_decode
from pyramid.httpexceptions import HTTPBadRequest, HTTPForbidden, HTTPFound, HTTPNotFound
from pyramid.security import has_permission

from openchordcharts.conv import (chart_to_json_dict, params_to_chart_data, params_to_chart_edit_data,
    params_to_charts_json_data)
from openchordcharts.helpers import get_login_url
from openchordcharts.model.chart import Chart, HistoryChart
from openchordcharts.utils import common_chromatic_keys


def chart(request):
    slug = request.matchdict.get('slug')
    if not slug:
        raise HTTPForbidden()
    data, errors = params_to_chart_data(request.params)
    if errors is not None:
        raise HTTPBadRequest(detail=errors)
    if data['revision']:
        chart = HistoryChart.find_one(dict(_id=data['revision']))
    else:
        chart = Chart.find_one(dict(slug=slug))
    if chart is None:
        raise HTTPNotFound()
    chart_json = chart_to_json_dict(chart)
    if request.matched_route.name == 'chart.json':
        return chart_json
    else:
        part_rows = []
        for part_name in chart.structure:
            rows = []
            chords = chart.parts[part_name]
            i = 0
            while i < len(chart.parts[part_name]):
                rows.append(chords[i:i + 8])
                i += 8
            part_rows.append(dict(
                name=part_name,
                rows=rows,
                ))
        template_string = pkg_resources.resource_string('openchordcharts', '/templates/eco/charts/show.eco')
        eco_template = eco.render(template_string, chart=chart_json, commonChromaticKeys=common_chromatic_keys,
            isLogged=request.user is not None, partRows=part_rows, routes={
                'chart': request.route_path('chart', slug=slug),
                'chart.delete': request.route_path('chart.delete', slug=slug),
                'chart.edit': request.route_path('chart.edit', slug=slug),
                'chart.history': request.route_path('chart.history', slug=slug),
                'chart.json': request.route_path('chart.json', slug=slug, _query=dict(
                    key=chart.key,
                    revision=data['revision'] or '',
                    )),
                'chart.undelete': request.route_path('chart.undelete', slug=slug),
                'login': get_login_url(request),
                },
            )
        return dict(
            eco_template=eco_template,
            )


def charts(request):
    settings = request.registry.settings
    spec = dict(
        is_deleted={'$exists': False},
        )
    charts = [chart_to_json_dict(chart) for chart in Chart.find(spec).sort('title').limit(settings['charts.limit'])]
    template_string = pkg_resources.resource_string('openchordcharts', '/templates/eco/charts/list.eco')
    eco_template = eco.render(template_string, charts=charts, isLogged=request.user is not None,
        routes={'chart.create': request.route_path('chart.create')})
    return dict(
        eco_template=eco_template,
        )


def charts_json(request):
    settings = request.registry.settings
    data, errors = params_to_charts_json_data(request.params)
    if errors is not None:
        raise HTTPBadRequest(detail=errors)
    spec = dict()
    if not data['include_deleted']:
        spec['is_deleted'] = {'$exists': False}
    title_slug = None
    if data['slug']:
        slug = data['slug']
        if slug:
            spec['slug'] = slug
    if data['title']:
        title_slug = slugify(data['title'])
        if title_slug:
            spec['keywords'] = Chart.get_search_by_keywords_spec(title_slug.split('-'))
    if data['user']:
        user = data['user']
        if user:
            spec['user'] = user
    return [chart_to_json_dict(chart) for chart in Chart.find(spec).sort('slug').limit(settings['charts.limit'])]


def create(request):
    if request.user is None or not has_permission('edit', request.root, request):
        raise HTTPForbidden()
    chart = Chart()
    if request.method == 'POST':
        params = variable_decode(request.POST)
        chart_data, chart_errors = params_to_chart_edit_data(params)
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
        chart_data=chart_data or {},
        chart_errors=chart_errors or {},
        form_action_url=request.route_path('chart.create'),
        )


def delete(request):
    if request.user is None or not has_permission('edit', request.root, request):
        raise HTTPForbidden()
    slug = request.matchdict.get('slug')
    if not slug:
        raise HTTPForbidden()
    chart = Chart.find_one(dict(slug=slug))
    if chart is None:
        raise HTTPNotFound()
    if chart.is_deleted:
        raise HTTPBadRequest(explanation=u'Chart is already deleted')
    chart.is_deleted = True
    chart.save(safe=True)
    return HTTPFound(location=request.route_path('chart', slug=chart.slug))


def edit(request):
    if request.user is None or not has_permission('edit', request.root, request):
        raise HTTPForbidden()
    slug = request.matchdict.get('slug')
    if not slug:
        raise HTTPForbidden()
    chart = Chart.find_one(dict(slug=slug))
    if chart is None:
        raise HTTPNotFound()
    if request.method == 'POST':
        params = variable_decode(request.POST)
        chart_data, chart_errors = params_to_chart_edit_data(params)
        if chart_errors is None:
            if not chart.equals(chart_data):
                history_chart = HistoryChart()
                history_chart.update_from_dict(chart.__dict__)
                history_chart.chart_id = chart._id
                history_chart.save(safe=True)
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


def history(request):
    slug = request.matchdict.get('slug')
    if not slug:
        raise HTTPForbidden()
    chart = Chart.find_one(dict(slug=slug))
    if chart is None:
        raise HTTPNotFound()
    history_charts_cursor = HistoryChart.find(dict(chart_id=chart._id)).sort('modified_at')
    return dict(
        chart=chart,
        history_charts_cursor=history_charts_cursor,
        )


def undelete(request):
    if request.user is None or not has_permission('edit', request.root, request):
        raise HTTPForbidden()
    slug = request.matchdict.get('slug')
    if not slug:
        raise HTTPForbidden()
    chart = Chart.find_one(dict(slug=slug))
    if chart is None:
        raise HTTPNotFound()
    if not chart.is_deleted:
        raise HTTPBadRequest(explanation=u'Chart is not deleted')
    chart.is_deleted = None
    chart.save(safe=True)
    return HTTPFound(location=request.route_path('chart', slug=chart.slug))
