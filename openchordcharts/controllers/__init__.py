# -*- coding: utf-8 -*-


from webob.dec import wsgify

from . import accounts, charts, users
from .. import router, templates


@wsgify
def index(req):
    return templates.render(req.ctx, '/index.mako')


def make_router(ctx):
    routings = [
        ('GET', '^/?$', index),
        ('GET', '^/charts/?$', charts.index),
        ('GET', '^/charts/(?P<slug>.+)/delete$', charts.delete),
        (('GET', 'POST'), '^/charts/(?P<slug>.+)/edit$', charts.edit),
        ('GET', '^/charts/(?P<slug>.+).json$', charts.view),
        ('GET', '^/charts/(?P<slug>.+)$', charts.view),
        ('GET', '^/charts/create$', charts.edit),
        ('GET', '^/users/(?P<slug>.+)$', users.view),
        ('GET', '^/logout/?$', accounts.logout),
        ]
    if ctx.conf['dummy_login.user_id'] is not None:
        routings.extend([
            ('GET', '^/login/?$', accounts.login_dummy),
            ])
    else:
        routings.extend([
            ('GET', '^/login/?$', accounts.login),
            ('GET', '^/login-callback/?$', accounts.login_callback),
            ])
    return router.make_router(*routings)
