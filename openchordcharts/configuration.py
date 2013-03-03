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


"""Paste INI configuration"""


import logging
import os
import urlparse

from biryani1 import strings
from biryani1.baseconv import (check, cleanup_line, default, empty_to_none, function, guess_bool, input_to_int,
    noop, make_input_to_url, pipe, struct)


def load_configuration(global_conf, app_conf):
    """Build the application configuration dict."""
    app_dir = os.path.dirname(os.path.abspath(__file__))
    conf = {}
    conf.update(strings.deep_decode(global_conf))
    conf.update(strings.deep_decode(app_conf))
    conf.update(check(struct(
        {
            'app_conf': default(app_conf),
            'app_dir': default(app_dir),
            'beaker.session.data_dir': empty_to_none,
            'beaker.session.lock_dir': empty_to_none,
            'cache_dir': default(os.path.join(os.path.dirname(app_dir), 'cache')),
            'cdn.url': default('http://localhost:7000'),
            'charts.limit': pipe(input_to_int, default(1000)),
            'database.host_name': default('localhost'),
            'database.name': default('openchordcharts'),
            'database.port': pipe(input_to_int, default(27017)),
            'debug': pipe(guess_bool, default(False)),
            'dummy_login.user_id': empty_to_none,
            'email_to': cleanup_line,
            'global_conf': default(global_conf),
            'google_analytics_key': empty_to_none,
            'log_level': pipe(
                default('WARNING'),
                function(lambda log_level: getattr(logging, log_level.upper())),
                ),
            'openid.api_key': empty_to_none,
            'openid.api_url': make_input_to_url(error_if_fragment=True, full=True),
            'package_name': default('openchordcharts'),
            'static_files': pipe(guess_bool, default(False)),
            'static_files_dir': default(os.path.join(app_dir, 'static')),
            },
        default='drop',
        drop_none_values=False,
        ))(conf))

    # Assets
    conf.update(check(struct(
        {
            'cdn.bootstrap.css': default(urlparse.urljoin(conf['cdn.url'], '/bootstrap/2.2.2/css/bootstrap.min.css')),
            'cdn.bootstrap-responsive.css': default(
                urlparse.urljoin(conf['cdn.url'], '/bootstrap/2.2.2/css/bootstrap-responsive.min.css')
                ),
            'cdn.bootstrap.js': default(urlparse.urljoin(conf['cdn.url'], '/bootstrap/2.2.2/js/bootstrap.js')),
            'cdn.jquery.js': default(urlparse.urljoin(conf['cdn.url'], '/jquery/jquery-1.9.0.min.js')),
            },
        default=noop,
        ))(conf))
    return conf
