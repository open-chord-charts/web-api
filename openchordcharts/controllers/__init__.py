# -*- coding: utf-8 -*-


from webob.dec import wsgify

from . import charts, users
from .. import router, templates


@wsgify
def index(req):
    return templates.render(req.ctx, '/index.mako')


def make_router():
    return router.make_router(
        ('GET', '^/?$', index),
        ('GET', '^/charts/?$', charts.index),
        ('GET', '^/charts/(?P<slug>.+)/edit$', charts.edit),
        ('GET', '^/charts/(?P<slug>.+).json$', charts.view),
        ('GET', '^/charts/(?P<slug>.+)$', charts.view),
        ('GET', '^/charts/create$', charts.edit),
        ('GET', '^/users/(?P<slug>.+)$', users.view))
