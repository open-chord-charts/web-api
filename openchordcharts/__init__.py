# -*- coding: utf-8 -*-

from pyramid.authentication import AuthTktAuthenticationPolicy
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
    config = Configurator(
        authentication_policy=authentication_policy,
        root_factory=Root,
        settings=settings,
        )

    config.set_request_factory(RequestWithUserAttribute)

    # API
    config.add_route('charts.json', '/api/1/charts.json')

    # Authentication
    config.add_route('login_callback', '/login-callback/')
    config.add_route('logout', '/logout/')

    config.add_route('index', '/')
    config.add_route('about', '/about')
    config.add_route('chart', '/charts/{slug}')
    config.add_route('charts', '/charts/')
    config.add_route('user', '/users/{slug}')
    config.add_route('users', '/users/')

    config.scan('openchordcharts.views')

    config.add_renderer('jsonp', JSONP(param_name='callback'))

    config.add_static_view('static', 'openchordcharts:static')

    config.add_subscriber('openchordcharts.subscribers.check_user_has_name', 'pyramid.events.NewRequest')

    return config.make_wsgi_app()
