# -*- coding: utf-8 -*-

from pyramid.exceptions import Forbidden
from pyramid.view import view_config

from openchordcharts.model.chart import Chart


@view_config(route_name='user', renderer='/user.mako')
def user(request):
    user_email = request.matchdict.get('user_email')
    if not user_email:
        raise Forbidden()
    user_charts = Chart.find(dict(user=user_email))
    return dict(
        user_charts=user_charts,
        )


@view_config(route_name='users')
def users(request):
    return {}
