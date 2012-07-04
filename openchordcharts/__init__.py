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
from pyramid.session import UnencryptedCookieSessionFactoryConfig

from openchordcharts.auth import RequestWithUserAttribute
from openchordcharts.conv import validate_settings
from openchordcharts.model import initialize_model
from openchordcharts.resources import Root
import openchordcharts.views
import openchordcharts.views.auth
import openchordcharts.views.auth.fake
import openchordcharts.views.auth.openidconnect
import openchordcharts.views.charts
import openchordcharts.views.users


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    settings = validate_settings(settings)
    initialize_model(settings)

    authentication_policy = AuthTktAuthenticationPolicy(settings['authentication.secret'])
    authorization_policy = ACLAuthorizationPolicy()
    session_factory = UnencryptedCookieSessionFactoryConfig(settings['authentication.secret'])
    config = Configurator(
        authentication_policy=authentication_policy,
        authorization_policy=authorization_policy,
        root_factory=Root,
        session_factory=session_factory,
        settings=settings,
        )

    config.set_request_factory(RequestWithUserAttribute)

    # Authentication
    if settings['authentication.fake_login']:
        config.add_route('fake_login', '/login-fake/')
        config.add_view(openchordcharts.views.auth.fake.login, route_name='fake_login')
    if settings['authentication.openid.client_id']:
        config.add_route('login_callback', '/login-callback/')
        config.add_view(openchordcharts.views.auth.openidconnect.login_callback, route_name='login_callback')
        config.add_route('openidconnect_login', '/login-openidconnect/')
        config.add_view(openchordcharts.views.auth.openidconnect.login, route_name='openidconnect_login')
    config.add_route('logout', '/logout/')
    config.add_view(openchordcharts.views.auth.logout, route_name='logout')

    config.add_route('index', '/')
    config.add_view(renderer='/index.mako', route_name='index')
    config.add_route('about', '/about')
    config.add_view(renderer='/about.mako', route_name='about')
    config.add_route('cache.manifest', '/cache.manifest')
    config.add_view(renderer='/cache_manifest.mako', route_name='cache.manifest')


    config.add_route('chart.create', '/charts/create')
    config.add_view(openchordcharts.views.charts.create, permission='edit', renderer='/chart_edit.mako',
        route_name='chart.create')
    config.add_route('chart.delete', '/charts/{slug}/delete')
    config.add_view(openchordcharts.views.charts.delete, permission='edit', route_name='chart.delete')
    config.add_route('chart.edit', '/charts/{slug}/edit')
    config.add_view(openchordcharts.views.charts.edit, permission='edit', renderer='/chart_edit.mako',
        route_name='chart.edit')
    config.add_route('chart.history', '/charts/{slug}/history')
    config.add_view(openchordcharts.views.charts.history, renderer='/chart_history.mako', route_name='chart.history')
    config.add_route('chart.json', '/charts/{slug}.json')
    config.add_view(openchordcharts.views.charts.chart, renderer='jsonp', route_name='chart.json')
    config.add_route('chart.undelete', '/charts/{slug}/undelete')
    config.add_view(openchordcharts.views.charts.undelete, permission='edit', route_name='chart.undelete')
    config.add_route('chart', '/charts/{slug}')
    config.add_view(openchordcharts.views.charts.chart, renderer='/chart.mako', route_name='chart')
    config.add_route('charts', '/charts/')
    config.add_view(openchordcharts.views.charts.charts, renderer='/charts.mako', route_name='charts')
    config.add_route('charts.json', '/charts.json')
    config.add_view(openchordcharts.views.charts.charts_json, renderer='jsonp', route_name='charts.json')

    config.add_route('user', '/users/{slug}')
    config.add_view(openchordcharts.views.users.user, renderer='/user.mako', route_name='user')

    config.scan('openchordcharts.views')

    config.add_renderer('jsonp', JSONP(param_name='callback'))

    config.add_static_view('static', 'openchordcharts:static')

    return config.make_wsgi_app()
