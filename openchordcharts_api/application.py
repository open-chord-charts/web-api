# -*- coding: utf-8 -*-


# Open Chord Charts -- Database of free chord charts
# By: Christophe Benz <contact@openchordcharts.org>
#
# Copyright (C) 2012, 2013, 2014 Christophe Benz
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


"""Middleware initialization"""


import re
import urllib

import webob

from . import contexts, controllers, environment, wsgihelpers


percent_encoding_re = re.compile('%[\dA-Fa-f]{2}')


# Middlewares

def cross_origin_resource_sharing_handler(app):
    """WSGI middleware that handles CORS headers."""
    def handle_cross_origin_resource_sharing(environ, start_response):
        req = webob.Request(environ)
        ctx = contexts.Ctx(req)
        try:
            headers = wsgihelpers.handle_cross_origin_resource_sharing(ctx)
        except webob.exc.HTTPException as exc:
            res = exc
            return res(environ, start_response)
        res = req.get_response(app)
        res.headers.update(headers)
        return res(environ, start_response)

    return handle_cross_origin_resource_sharing


def request_query_encoding_fixer(app):
    """WSGI middleware that repairs a badly encoded query in request URL."""
    def fix_request_query_encoding(environ, start_response):
        req = webob.Request(environ)
        query_string = req.query_string
        if query_string is not None:
            try:
                urllib.unquote(query_string).decode('utf-8')
            except UnicodeDecodeError:
                req.query_string = percent_encoding_re.sub(
                    lambda match: urllib.quote(urllib.unquote(match.group(0)).decode('iso-8859-1').encode('utf-8')),
                    query_string)
        return app(req.environ, start_response)

    return fix_request_query_encoding


# App factory

def make_app(global_conf, **app_conf):
    """Create a WSGI application and return it

    ``global_conf``
        The inherited configuration for this application. Normally from
        the [DEFAULT] section of the Paste ini file.

    ``app_conf``
        The application's local configuration. Normally specified in
        the [app:<name>] section of the Paste ini file (where <name>
        defaults to main).
    """
    # Configure the environment and fill conf dictionary.
    environment.load_environment(global_conf, app_conf)

    # Dispatch request to controllers.
    app = controllers.make_router()

    # Handle CORS headers
    app = cross_origin_resource_sharing_handler(app)

    # Repair badly encoded query in request URL.
    app = request_query_encoding_fixer(app)

    return app
