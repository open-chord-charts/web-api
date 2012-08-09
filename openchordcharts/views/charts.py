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


import json
import pkg_resources

import eco
from pyramid.httpexceptions import HTTPBadRequest, HTTPForbidden, HTTPNotFound
from pyramid.security import has_permission

from openchordcharts.conv import (chart_to_json_dict, json_to_chart_data, params_to_chart_data,
    params_to_charts_json_data, user_to_json_dict)
from openchordcharts.helpers import get_login_url
from openchordcharts.model.chart import Chart, HistoryChart


common_chromatic_keys = ['Ab', 'A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G']


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
        chart_json['parts'] = part_rows
        template_string = pkg_resources.resource_string('openchordcharts', '/templates/eco/charts/show.eco')
        eco_template = eco.render(template_string, chart=chart_json, commonChromaticKeys=common_chromatic_keys, routes={
            'chart': request.route_path('chart', slug=slug),
            'chart.edit': request.route_path('chart.edit', slug=slug),
            'chart.history': request.route_path('chart.history', slug=slug),
            'chart.json': request.route_path('chart.json', slug=slug, _query=dict(
                key=chart.key,
                revision=data['revision'] or '',
                )),
            'login': get_login_url(request),
            }, user=user_to_json_dict(request.user),
            )
        return dict(
            eco_template=eco_template,
            )


def charts(request):
    settings = request.registry.settings
    spec = {}
    charts = [chart_to_json_dict(chart) for chart in Chart.find(spec).sort('title').limit(settings['charts.limit'])]
    template_string = pkg_resources.resource_string('openchordcharts', '/templates/eco/charts/list.eco')
    eco_template = eco.render(template_string, charts=charts, routes={
        'chart.create': request.route_path('chart.create'),
        }, user=user_to_json_dict(request.user),
        )
    return dict(
        eco_template=eco_template,
        )


def charts_json(request):
    settings = request.registry.settings
    fizzle = request.matchdict.get('fizzle')
    if fizzle:
        slug = fizzle[0]
        if not slug:
            raise HTTPNotFound()
        if request.method == 'GET':
            chart = Chart.find_one(dict(slug=slug))
            if chart is None:
                raise HTTPNotFound()
            return chart_to_json_dict(chart)
        elif request.method == 'PUT':
            if request.user is None or not has_permission('edit', request.root, request):
                raise HTTPForbidden()
            chart = Chart.find_one(dict(slug=slug))
            if chart is None:
                raise HTTPNotFound()
            chart_json = json.loads(request.body)
            chart_data, chart_errors = json_to_chart_data(chart_json)
            if chart_errors:
                # TODO Put HTTP error code in response.
                return dict(errors=chart_errors)
            if chart.has_same_data_than(chart_data):
                return chart_to_json_dict(chart)
            history_chart = HistoryChart()
            history_chart.update_from_dict(chart.__dict__)
            history_chart.chart_id = chart._id
            history_chart.save(safe=True)
            chart.update_from_dict(chart_data)
            chart.save(safe=True)
            return chart_to_json_dict(chart)
        else:
            raise HTTPBadRequest(explanation=u'Unsupported HTTP method')
    else:
        data, errors = params_to_charts_json_data(dict(
            q=request.params.get('q'),
            slugs=request.params.getall('slug'),
            user=request.params.get('user'),
            ))
        if errors is not None:
            raise HTTPBadRequest(detail=errors)
        spec = dict()
        if data['slugs']:
            spec['slug'] = data['slugs'][0] if len(data['slugs']) == 1 else {'$in': data['slugs']}
        if data['user']:
            user = data['user']
            if user:
                spec['user'] = user
        return [chart_to_json_dict(chart) for chart in Chart.find(spec).sort('slug').limit(settings['charts.limit'])]


def edit(request):
    if request.user is None or not has_permission('edit', request.root, request):
        raise HTTPForbidden()
    slug = request.matchdict.get('slug')
    if not slug:
        raise HTTPForbidden()
    chart = Chart.find_one(dict(slug=slug))
    if chart is None:
        raise HTTPNotFound()
    return dict(
        eco_template=u'',
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
