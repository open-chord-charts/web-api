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
from .. import templates, wsgi_helpers


@wsgify
def view(req):
    slug = req.urlvars.get('slug')
    if slug is None:
        return wsgi_helpers.forbidden()
    user = req.ctx.db.accounts.find_one({'slug': slug})
    if user is None:
        return wsgi_helpers.not_found()
    charts_cursor = Chart.find({'user': slug}).limit(req.ctx.conf['charts.limit'])
    return templates.render(
        req.ctx,
        '/users/view.mako',
        charts_cursor=charts_cursor,
        )
