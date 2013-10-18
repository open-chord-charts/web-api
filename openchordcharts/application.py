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


"""Middleware initialization"""


import logging
import sys

from beaker.middleware import SessionMiddleware
from paste.cascade import Cascade
from paste.urlparser import StaticURLParser
from weberror.errormiddleware import ErrorMiddleware

from . import configuration, context, controllers, database, templates


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
    app_ctx = context.Context()
    app_ctx.conf = configuration.load_configuration(global_conf, app_conf)
    logging.basicConfig(level=app_ctx.conf['log_level'], stream=sys.stdout)
    app_ctx.db = database.load_database(app_ctx)
    app_ctx.templates = templates.load_templates(app_ctx)
    database.ensure_indexes(app_ctx)
    app = controllers.make_router(app_ctx)
    app = SessionMiddleware(app, app_ctx.conf)
    app = context.make_add_context_to_request(app, app_ctx)
    if not app_ctx.conf['debug'] and app_ctx.conf['email_to']:
        app = ErrorMiddleware(
            app,
            error_email=app_ctx.conf['email_to'],
            error_log=app_ctx.conf.get('error_log', None),
            error_message=app_ctx.conf.get('error_message', u'An internal server error occurred'),
            error_subject_prefix=app_ctx.conf.get('error_subject_prefix', u'Web application error: '),
            from_address=app_ctx.conf['from_address'],
            smtp_server=app_ctx.conf.get('smtp_server', 'localhost'),
        )
    if app_ctx.conf['static_files']:
        # Serve static files.
        app = Cascade([StaticURLParser(app_ctx.conf['static_files_dir']), app])
    app.ctx = app_ctx
    return app
