# -*- coding: utf-8 -*-


# Open Chord Charts -- Database of free chord charts
# By: Christophe Benz <contact@openchordcharts.org>
#
# Copyright (C) 2012-2013 Christophe Benz
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


"""Index controller function, router declaration."""


from webob.dec import wsgify

from . import accounts, charts, users
from .. import router, templates


@wsgify
def index(req):
    return templates.render(req.ctx, '/index.mako')


def make_router(ctx):
    routings = [
        ('GET', '^/?$', index),
        ('GET', '^/charts/?$', charts.index),
        (('GET', 'POST'), '^/charts/create$', charts.edit),
        ('GET', '^/users/(?P<username>[^/]+)/charts/(?P<chart_slug>[^/]+).json$', charts.view, {'is_json': True}),
        ('GET', '^/users/(?P<username>[^/]+)/charts/(?P<chart_slug>[^/]+)$', charts.view, {'is_json': False}),
        (('GET', 'POST'), '^/users/(?P<username>[^/]+)/charts/(?P<chart_slug>[^/]+)/edit$', charts.edit),
        ('GET', '^/users/(?P<username>[^/]+)/charts/(?P<chart_slug>[^/]+)/delete$', charts.delete),
        ('GET', '^/users/(?P<username>[^/]+)/charts/?$', users.view),
        ('GET', '^/logout/?$', accounts.logout),
        ]
    if ctx.conf['dummy_login.username'] is not None:
        routings.extend([
            ('GET', '^/login/?$', accounts.login_dummy),
            ])
    return router.make_router(*routings)
