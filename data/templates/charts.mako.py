# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1341923546.516567
_enable_loop = True
_template_filename = '/home/cbenz/dev/projets/openchordcharts/openchordcharts/templates/charts.mako'
_template_uri = '/charts.mako'
_source_encoding = 'utf-8'
from markupsafe import escape_silent
_exports = ['page_title', u'title']


# SOURCE LINE 23

from pyramid.security import has_permission
from webhelpers.html.tools import highlight

from openchordcharts.helpers import get_login_url


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    pass
def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'site.mako', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        parent = context.get('parent', UNDEFINED)
        def title():
            return render_title(context.locals_(__M_locals))
        self = context.get('self', UNDEFINED)
        request = context.get('request', UNDEFINED)
        dict = context.get('dict', UNDEFINED)
        charts_cursor = context.get('charts_cursor', UNDEFINED)
        nb_deleted_charts = context.get('nb_deleted_charts', UNDEFINED)
        data = context.get('data', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 21
        __M_writer(u'\n\n')
        # SOURCE LINE 28
        __M_writer(u'\n\n\n')
        # SOURCE LINE 31
        __M_writer(u'\n\n\n')
        # SOURCE LINE 36
        __M_writer(u'\n\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'title'):
            context['self'].title(**pageargs)
        

        # SOURCE LINE 41
        __M_writer(u'\n\n\n')
        # SOURCE LINE 44
        if not data['q']:
            # SOURCE LINE 45
            if has_permission('edit', request.root, request):
                # SOURCE LINE 46
                __M_writer(u'<p><a class="btn" href="')
                __M_writer(escape_silent(request.route_path('chart.create')))
                __M_writer(u'">Add a new chart</a></p>\n')
                # SOURCE LINE 47
            else:
                # SOURCE LINE 48
                __M_writer(u'<p><a class="btn" data-content="Creation is restricted to authenticated users." href="')
                __M_writer(escape_silent(get_login_url(request)))
                __M_writer(u'" ')
                # SOURCE LINE 49
                __M_writer(u'rel="nofollow popover" title="Please login first!">Add a new chart</a></p>\n')
                pass
            pass
        # SOURCE LINE 52
        __M_writer(u'\n<div class="page-header">\n  <h1>')
        def ccall(caller):
            def body():
                __M_writer = context.writer()
                return ''
            return [body]
        context.caller_stack.nextcaller = runtime.Namespace('caller', context, callables=ccall(__M_caller))
        try:
            # SOURCE LINE 54
            __M_writer(escape_silent(self.page_title()))
        finally:
            context.caller_stack.nextcaller = None
        __M_writer(escape_silent(u' (including deleted)' if data['include_deleted'] else ''))
        __M_writer(u'</h1>\n</div>\n\n')
        # SOURCE LINE 57
        if not data['include_deleted'] and not data['q'] and has_permission('edit', request.root, request) and \
  nb_deleted_charts:
            # SOURCE LINE 59
            __M_writer(u'<div class="alert alert-block">\n  <a class="close" data-dismiss="alert">\xd7</a>\n  <h4 class="alert-heading">Warning!</h4>\n  <p>There are deleted charts.</p>\n  <p><a class="btn" href="')
            # SOURCE LINE 63
            __M_writer(escape_silent(request.route_path('charts', _query=dict(include_deleted=1))))
            __M_writer(u'">Display them too</a></p>\n</div>\n')
            pass
        # SOURCE LINE 66
        __M_writer(u'\n')
        # SOURCE LINE 67
        if charts_cursor.count():
            # SOURCE LINE 68
            __M_writer(u'<ul>\n')
            # SOURCE LINE 69
            for chart in charts_cursor:
                # SOURCE LINE 70
                __M_writer(u'  <li><a href="')
                __M_writer(escape_silent(request.route_path('chart', slug=chart.slug)))
                __M_writer(u'">')
                # SOURCE LINE 71
                __M_writer(escape_silent(highlight(chart.title, data['q'].split()) if data['q'] else chart.title))
                # SOURCE LINE 72
                __M_writer(escape_silent(u' (deleted)' if chart.is_deleted else ''))
                __M_writer(u'</a></li>\n')
                pass
            # SOURCE LINE 74
            __M_writer(u'</ul>\n')
            # SOURCE LINE 75
        else:
            # SOURCE LINE 76
            __M_writer(u'<p>No charts found.</p>\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_page_title(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        data = context.get('data', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 34
        __M_writer(u'\n')
        # SOURCE LINE 35
        __M_writer(escape_silent(u'Results for "{0}"'.format(data['q']) if data['q'] else u'Charts'))
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_title(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        self = context.get('self', UNDEFINED)
        parent = context.get('parent', UNDEFINED)
        def title():
            return render_title(context)
        __M_writer = context.writer()
        # SOURCE LINE 39
        __M_writer(u'\n')
        def ccall(caller):
            def body():
                __M_writer = context.writer()
                return ''
            return [body]
        context.caller_stack.nextcaller = runtime.Namespace('caller', context, callables=ccall(__M_caller))
        try:
            # SOURCE LINE 40
            __M_writer(escape_silent(parent.title()))
        finally:
            context.caller_stack.nextcaller = None
        __M_writer(u': ')
        def ccall(caller):
            def body():
                __M_writer = context.writer()
                return ''
            return [body]
        context.caller_stack.nextcaller = runtime.Namespace('caller', context, callables=ccall(__M_caller))
        try:
            __M_writer(escape_silent(self.page_title()))
        finally:
            context.caller_stack.nextcaller = None
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


