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


from webob.dec import wsgify

from ..model.chart import Chart
from .. import conv, templates, wsgi_helpers


@wsgify
def edit(req):
#    if req.user is None:
#        return wsgi_helpers.forbidden(req.ctx)
    slug = req.urlvars.get('slug')
    if slug is None:
        return wsgi_helpers.forbidden(req.ctx)
    chart = Chart.find_one({'slug': slug})
    if chart is None:
        return wsgi_helpers.not_found(req.ctx)
    return templates.render(
        req.ctx,
        '/charts/edit.mako',
        chart=chart,
        )


@wsgify
def index(req):
    charts_cursor = Chart.find().sort('title').limit(req.ctx.conf['charts.limit'])
    # TODO Implement search.
    data = {'q': None}
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
    data, errors = conv.params_to_chart_data(req.params)
    if errors is not None:
        return wsgi_helpers.bad_request(req.ctx, comment=errors)
    chart = Chart.find_one(dict(slug=slug))
    if chart is None:
        return wsgi_helpers.not_found(req.ctx)
    chart_json = conv.chart_to_json_dict(chart)
    if req.path.endswith('.json'):
        return wsgi_helpers.respond_json(req.ctx, chart_json)
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
        return templates.render(
            req.ctx,
            '/charts/view.mako',
            chart=chart,
            part_rows=part_rows,
            )
