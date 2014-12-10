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

from formencode import variabledecode
from biryani1.baseconv import check
from webob.dec import wsgify

from ..model.account import Account
from ..model.chart import Chart
from .. import chart_render, conv, templates, wsgi_helpers


@wsgify
def delete(req):
    user = req.ctx.find_user()
    if user is None:
        return wsgi_helpers.forbidden(req.ctx)
    slug = req.urlvars.get('slug')
    spec = {
        'is_deleted': {'$exists': False},
        'slug': slug,
        }
    chart = Chart.find_one(spec)
    if chart is None:
        return wsgi_helpers.not_found(req.ctx)
    if chart.account_id != user._id:
        return wsgi_helpers.forbidden(req.ctx)
    chart.is_deleted = True
    chart.save(safe=True)
    return wsgi_helpers.redirect(req.ctx, location='/charts/')


@wsgify
def edit(req):
    user = req.ctx.find_user()
    if user is None:
        return wsgi_helpers.forbidden(req.ctx)
    slug = req.urlvars.get('slug')
    chart = data = errors = inputs = None
    if not req.path.endswith('/create'):
        spec = {
            'is_deleted': {'$exists': False},
            'slug': slug,
            }
        chart = Chart.find_one(spec)
        if chart is None:
            return wsgi_helpers.not_found(req.ctx)
        if chart.account_id != user._id:
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
                chart.account_id = user._id
            for key, value in data.iteritems():
                setattr(chart, key, value)
            chart.save(safe=True)
            assert chart.slug is not None
            return wsgi_helpers.redirect(req.ctx, location='/charts/{0}'.format(chart.slug))
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
    spec = {
        'is_deleted': {'$exists': False},
        }
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
    slug = req.urlvars.get('slug')
    if not slug:
        return wsgi_helpers.forbidden(req.ctx)
    data, errors = conv.params_to_chart_view_data(req.params, state=conv.default_state)
    if errors is not None:
        return wsgi_helpers.bad_request(req.ctx, comment=errors)
    spec = {
        'is_deleted': {'$exists': False},
        'slug': slug,
        }
    chart = Chart.find_one(spec)
    if chart is None or chart.is_deleted:
        return wsgi_helpers.not_found(req.ctx)
    chart_json = check(conv.chart_to_json_dict(chart, state=conv.default_state))
    if req.path.endswith('.json'):
        return wsgi_helpers.respond_json(req.ctx, chart_json)
    else:
        chart_owner = Account.find_one({'_id': chart.account_id}) if chart.account_id is not None else None
        return templates.render(
            req.ctx,
            '/charts/view.mako',
            chart=chart,
            chart_owner=chart_owner,
            data=data,
            )
