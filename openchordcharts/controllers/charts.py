# -*- coding: utf-8 -*-


# Open Chord Charts -- Database of free chord charts
# By: Christophe Benz <contact@openchordcharts.org>
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


"""Charts controller functions."""


import re

from biryani1.baseconv import check
from formencode import variabledecode
from webob.dec import wsgify

from ..model.chart import Chart
from .. import chart_render, conv, templates, wsgi_helpers


@wsgify
def delete(req):
    if req.ctx.user is None:
        return wsgi_helpers.forbidden(req.ctx)
    chart_slug = req.urlvars.get('chart_slug')
    chart = Chart.find_one({'slug': chart_slug})
    if chart is None:
        return wsgi_helpers.not_found(req.ctx)
    if chart.account_id != req.ctx.user._id:
        return wsgi_helpers.forbidden(req.ctx)
    chart.delete(safe=True)
    return wsgi_helpers.redirect(req.ctx, location='/users/{}/charts/'.format(req.ctx.user.username))


@wsgify
def edit(req):
    if req.ctx.user is None:
        return wsgi_helpers.forbidden(req.ctx)
    chart_slug = req.urlvars.get('chart_slug')
    chart = data = errors = inputs = None
    if not req.path.endswith('/create'):
        chart = Chart.find_one({'slug': chart_slug})
        if chart is None:
            return wsgi_helpers.not_found(req.ctx)
        if chart.account_id != req.ctx.user._id:
            return wsgi_helpers.forbidden(req.ctx)
    if req.method == 'POST':
        inputs = variabledecode.variable_decode(req.POST)
        inputs['parts'] = inputs.get('part')
        data, errors = conv.inputs_to_chart_edit_data(inputs)
        missing_parts = chart_render.build_missing_parts(data)
        if missing_parts:
            if inputs['parts'] is None:
                inputs['parts'] = {}
            inputs['parts'].update({part_name: '' for part_name in missing_parts})
        if errors is None:
            if req.path.endswith('/create'):
                chart = Chart()
                chart.account_id = req.ctx.user._id
            for key, value in data.iteritems():
                setattr(chart, key, value)
            chart.save(safe=True)
            assert chart.slug is not None
            return wsgi_helpers.redirect(req.ctx, location='/users/{}/charts/{}'.format(
                req.ctx.user.username, chart.slug))
    else:
        inputs = check(conv.chart_to_edit_inputs(chart))
    return templates.render(
        req.ctx,
        '/charts/edit.mako',
        chart=chart,
        data=data,
        errors=errors or {},
        inputs=inputs or {},
        )


@wsgify
def index(req):
    data, errors = conv.params_to_chart_index_data(req.params, state=conv.default_state)
    if errors is not None:
        return wsgi_helpers.bad_request(req.ctx, comment=errors)
    spec = {}
    keywords = None
    if data['q'] is not None:
        keywords = data['q'].strip().split()
        spec['keywords'] = {'$all': [re.compile(u'^{0}'.format(re.escape(keyword))) for keyword in keywords]}
    charts_cursor = Chart.find(spec).sort('slug').limit(req.ctx.conf['charts.limit'])
    return templates.render(
        req.ctx,
        '/charts/index.mako',
        charts_cursor=charts_cursor,
        data=data,
        )


@wsgify
def view(req):
    chart_slug = req.urlvars.get('chart_slug')
    assert chart_slug is not None
    data, errors = conv.params_to_chart_view_data(req.params, state=conv.default_state)
    if errors is not None:
        return wsgi_helpers.bad_request(req.ctx, comment=errors)
    chart = Chart.find_one({'slug': chart_slug})
    if chart is None:
        return wsgi_helpers.not_found(req.ctx)
    chart_json = check(conv.chart_to_json_dict(chart, state=conv.default_state))
    if req.path.endswith('.json'):
        return wsgi_helpers.respond_json(req.ctx, chart_json)
    else:
        return templates.render(
            req.ctx,
            '/charts/view.mako',
            chart=chart,
            data=data,
            )
