# -*- coding: utf-8 -*-


# Open Chord Charts -- Database of free chord charts
# By: Christophe Benz <contact@openchordcharts.org>
#
# Copyright (C) 2012, 2013, 2014, 2015 Christophe Benz
# https://github.com/openchordcharts/
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

import webob

from . import contexts, wsgihelpers


def make_router(*routings):
    """Return a WSGI application that dispatches requests to controllers """
    routes = []
    for routing in routings:
        methods, regex, app = routing[:3]
        if isinstance(methods, basestring):
            methods = (methods,)
        vars = routing[3] if len(routing) >= 4 else {}
        routes.append((methods, re.compile(unicode(regex)), app, vars))

    def router(environ, start_response):
        """Dispatch request to controllers."""
        req = webob.Request(environ)
        split_path_info = req.path_info.split('/')
        if split_path_info[0]:
            # When path_info doesn't start with a "/" this is an error or a attack => Reject request.
            # An example of an URL with such a invalid path_info: http://127.0.0.1http%3A//127.0.0.1%3A80/result?...
            ctx = contexts.Ctx(req)
            return wsgihelpers.bad_request(ctx, message=ctx._(u'Invalid path: {}').format(req.path_info))(
                environ, start_response)
        for methods, regex, app, vars in routes:
            if methods is None or req.method in methods:
                match = regex.match(req.path_info)
                if match is not None:
                    if getattr(req, 'urlvars', None) is None:
                        req.urlvars = {}
                    req.urlvars.update(match.groupdict())
                    req.urlvars.update(vars)
                    req.script_name += req.path_info[:match.end()]
                    req.path_info = req.path_info[match.end():]
                    return app(req.environ, start_response)
        ctx = contexts.Ctx(req)
        return wsgihelpers.not_found(ctx, message=ctx._(u'URL matched no route'))(environ, start_response)

    return router
