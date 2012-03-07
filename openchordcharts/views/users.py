# -*- coding: utf-8 -*-

from pyramid.exceptions import Forbidden, NotFound
from pyramid.view import view_config

from openchordcharts.model.chart import Chart
from openchordcharts.model.user import User


@view_config(route_name='user', renderer='/user.mako')
def user(request):
    slug = request.matchdict.get('slug')
    if not slug:
        raise Forbidden()
    user = User.find_one(dict(slug=slug))
    if user is None:
        raise NotFound()
    user_charts = Chart.find(dict(user=slug))
    return dict(
        user_charts=user_charts,
        )


@view_config(route_name='users')
def users(request):
    return {}
