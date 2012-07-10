# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1341923204.224533
_enable_loop = True
_template_filename = u'/home/cbenz/dev/projets/openchordcharts/openchordcharts/templates/navbar.mako'
_template_uri = u'/navbar.mako'
_source_encoding = 'utf-8'
from markupsafe import escape_silent
_exports = []


# SOURCE LINE 23

from openchordcharts.helpers import get_login_url


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        dict = context.get('dict', UNDEFINED)
        request = context.get('request', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 21
        __M_writer(u'\n\n')
        # SOURCE LINE 25
        __M_writer(u'\n\n\n<div class="navbar navbar-fixed-top">\n  <div class="navbar-inner">\n    <div class="container">\n      <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">\n        <span class="icon-bar"></span>\n        <span class="icon-bar"></span>\n        <span class="icon-bar"></span>\n      </a>\n      <a class="brand" href="')
        # SOURCE LINE 36
        __M_writer(escape_silent(request.route_path('index')))
        __M_writer(u'">Open Chord Charts (dev)</a>\n      <div class="nav-collapse">\n        <ul class="nav">\n          <li')
        # SOURCE LINE 39
        __M_writer(u' class="active"' if request.matched_route.name == 'charts' else '' )
        __M_writer(u'>\n            <a href="')
        # SOURCE LINE 40
        __M_writer(escape_silent(request.route_path('charts')))
        __M_writer(u'">Charts</a>\n          </li>\n        </ul>\n        <form action="')
        # SOURCE LINE 43
        __M_writer(escape_silent(request.route_path('charts')))
        __M_writer(u'" class="navbar-search pull-left">\n          <input class="search-query" name="q" placeholder="Search (ex: All of me)" type="text" value="')
        # SOURCE LINE 44
        __M_writer(escape_silent(request.GET.get('q', '')))
        __M_writer(u'">\n        </form>\n')
        # SOURCE LINE 46
        if request.user:
            # SOURCE LINE 47
            __M_writer(u'        <div class="btn-group pull-right">\n          <a class="btn dropdown-toggle" data-toggle="dropdown" href="#">\n            <i class="icon-user"></i> ')
            # SOURCE LINE 49
            __M_writer(escape_silent(request.user.email))
            __M_writer(u'\n            <span class="caret"></span>\n          </a>\n          <ul class="dropdown-menu">\n            <li><a href="')
            # SOURCE LINE 53
            __M_writer(escape_silent(request.route_path('user', slug=request.user.slug)))
            __M_writer(u'">Profile</a></li>\n            <li class="divider"></li>\n            <li><a href="')
            # SOURCE LINE 55
            __M_writer(escape_silent(request.route_path('logout', _query=dict(state=request.current_route_path()))))
            __M_writer(u'" ')
            # SOURCE LINE 56
            __M_writer(u'rel="nofollow">Logout</a></li>\n          </ul>\n        </div>\n')
            # SOURCE LINE 59
        else:
            # SOURCE LINE 60
            __M_writer(u'        <ul class="nav pull-right">\n          <li>\n            <a href="')
            # SOURCE LINE 62
            __M_writer(escape_silent(get_login_url(request)))
            __M_writer(u'" rel="nofollow">Login</a>\n          </li>\n        </ul>\n')
            pass
        # SOURCE LINE 66
        __M_writer(u'      </div>\n    </div>\n  </div>\n</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


