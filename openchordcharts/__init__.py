# -*- coding: utf-8 -*-

import pymongo

from pyramid.config import Configurator
from pyramid.events import subscriber
from pyramid.events import NewRequest

from openchordcharts.model import initialize_model
from openchordcharts.resources import Root


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory=Root, settings=settings)
    initialize_model(settings)
    config.add_route('index', '/')
    config.add_route('chart', '/charts/{title}')
    config.add_route('charts', '/charts/')
    config.add_subscriber('openchordcharts.model.add_request_attributes', 'pyramid.events.NewRequest')
    config.scan('openchordcharts')
    return config.make_wsgi_app()
