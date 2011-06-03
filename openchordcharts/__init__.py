from pyramid.config import Configurator
from openchordcharts.resources import Root

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory=Root, settings=settings)
    config.add_view('openchordcharts.views.my_view',
                    context='openchordcharts:resources.Root',
                    renderer='openchordcharts:templates/mytemplate.pt')
    config.add_static_view('static', 'openchordcharts:static')
    return config.make_wsgi_app()

