from gridfs import GridFS
import pymongo

from pyramid.config import Configurator
from pyramid.events import subscriber
from pyramid.events import NewRequest

from openchordcharts.resources import Root


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory=Root, settings=settings)
    conn = pymongo.Connection(settings['db_uri'])
    config.registry.settings['db_conn'] = conn
    config.add_subscriber(add_mongo_db, NewRequest)
    config.add_route('index', '/')
    config.scan('openchordcharts')
    config.add_static_view('static', 'openchordcharts:static')
    return config.make_wsgi_app()


# From http://docs.pylonsproject.org/projects/pyramid_cookbook/dev/mongo.html
def add_mongo_db(event):
    settings = event.request.registry.settings
    db = settings['db_conn'][settings['db_name']]
    event.request.db = db
    event.request.fs = GridFS(db)
