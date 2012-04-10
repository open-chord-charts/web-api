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


from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.renderers import JSONP

from openchordcharts.model import initialize_model
from openchordcharts.resources import Root
from openchordcharts.security import RequestWithUserAttribute


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    initialize_model(settings)

    authentication_policy = AuthTktAuthenticationPolicy(settings['authentication.secret'])
    authorization_policy = ACLAuthorizationPolicy()
    config = Configurator(
        authentication_policy=authentication_policy,
        authorization_policy=authorization_policy,
        root_factory=Root,
        settings=settings,
        )

    config.set_request_factory(RequestWithUserAttribute)

    # API
    config.add_route('charts.json', '/api/1/charts.json')

    # Authentication
    if settings['authentication.fake_login']:
        config.add_route('fake_login', '/fake-login/')
    config.add_route('login_callback', '/login-callback/')
    config.add_route('logout', '/logout/')

    config.add_route('index', '/')
    config.add_route('about', '/about')
    config.add_route('chart.edit', '/charts/{slug}/edit')
    config.add_route('chart.json', '/charts/{slug}.json')
    config.add_route('chart', '/charts/{slug}')
    config.add_route('charts', '/charts/')
    config.add_route('user', '/users/{slug}')
    config.add_route('users', '/users/')

    config.scan('openchordcharts.views')

    config.add_renderer('jsonp', JSONP(param_name='callback'))

    config.add_static_view('static', 'openchordcharts:static')

    return config.make_wsgi_app()
