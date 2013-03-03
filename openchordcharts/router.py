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


"""Helpers for URLs"""


import re

from webob.dec import wsgify

from . import wsgi_helpers


def make_router(*routings):
    """Return a WSGI application that dispatches requests to controllers."""
    routes = []
    for routing in routings:
        methods, regex, app = routing[:3]
        if isinstance(methods, basestring):
            methods = (methods,)
        vars = routing[3] if len(routing) >= 4 else {}
        routes.append((methods, re.compile(regex), app, vars))

    @wsgify
    def router(req):
        """Dispatch request to controllers."""
        split_path_info = req.path_info.split('/')
        assert not split_path_info[0], split_path_info
        for methods, regex, app, vars in routes:
            if methods is None or req.method in methods:
                match = regex.match(req.path_info)
                if match is not None:
                    if getattr(req, 'urlvars', None) is None:
                        req.urlvars = {}
                    req.urlvars.update(dict(
                        (name, value.decode('utf-8') if value is not None else None)
                        for name, value in match.groupdict().iteritems()
                        ))
                    req.urlvars.update(vars)
                    req.script_name += req.path_info[:match.end()]
                    req.path_info = req.path_info[match.end():]
                    return req.get_response(app)
        return wsgi_helpers.not_found(req.ctx)
    return router
