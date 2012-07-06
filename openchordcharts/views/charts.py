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


from biryani.baseconv import check, cleanup_line
from biryani.strings import slugify
from formencode.variabledecode import variable_decode
from pyramid.httpexceptions import HTTPBadRequest, HTTPForbidden, HTTPFound, HTTPNotFound
from pyramid.security import has_permission

from openchordcharts.conv import (chart_to_json_dict, params_to_chart_data, params_to_chart_edit_data,
    params_to_charts_data)
from openchordcharts.model.chart import Chart, HistoryChart


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
    if data['key'] is not None and data['key'] != chart.key:
        original_key = chart.key
        chart.transpose(data['key'])
    else:
        original_key = None
    if request.matched_route.name == 'chart.json':
        return chart_to_json_dict(chart)
    else:
        return dict(
            chart=chart,
            data=data,
            original_key=original_key,
            slug=slug,
            )


def charts(request):
    settings = request.registry.settings
    data, errors = params_to_charts_data(request.params)
    if errors is not None:
        raise HTTPBadRequest(detail=errors)
    spec = dict()
    if data['q']:
        q_slug = slugify(data['q'])
        if q_slug:
            spec['keywords'] = Chart.get_search_by_keywords_spec(q_slug.split('-'))
    if not data['include_deleted']:
        spec['is_deleted'] = {'$exists': False}
    charts_cursor = Chart.find(spec).sort('title').limit(int(settings['charts.limit']))
    nb_deleted_charts = Chart.find(dict(is_deleted=True)).count()
    return dict(
        charts_cursor=charts_cursor,
        data=data,
        nb_deleted_charts=nb_deleted_charts,
        )


def charts_json(request):
    spec = {}
    title_slug = None
    if request.GET.get('slug'):
        slug = check(cleanup_line(request.GET['slug']))
        if slug:
            spec['slug'] = slug
    if request.GET.get('title'):
        title_slug = slugify(request.GET['title'])
        if title_slug:
            spec['keywords'] = Chart.get_search_by_keywords_spec(title_slug.split('-'))
    if request.GET.get('user'):
        user = check(cleanup_line(request.GET['user']))
        if user:
            spec['user'] = user
    return [chart_to_json_dict(chart) for chart in Chart.find(spec)]


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
        chart_data=chart_data,
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
