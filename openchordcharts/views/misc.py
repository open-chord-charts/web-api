# -*- coding: utf-8 -*-


from pyramid.view import view_config


@view_config(route_name='about', renderer='/about.mako')
def about(request):
    return {}
