# -*- coding: utf-8 -*-

from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig

from openchordcharts.model import initialize_model
from openchordcharts.resources import Root


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    my_session_factory = UnencryptedCookieSessionFactoryConfig(settings['session.secret'])
    config = Configurator(
        root_factory=Root,
        session_factory=my_session_factory,
        settings=settings,
        )
    initialize_model(settings)
    config.add_route('index', '/')
    config.add_route('login_callback', '/login-callback/')
    config.add_route('logout', '/logout/')
    config.add_route('chart', '/charts/{slug}')
    config.add_route('charts', '/charts/')
    config.add_route('user', '/users/{user_email}')
    config.add_route('users', '/users/')
    config.add_static_view('static', 'openchordcharts:static')
    config.add_subscriber('openchordcharts.model.add_request_attributes', 'pyramid.events.NewRequest')
    config.scan('openchordcharts')
    return config.make_wsgi_app()
