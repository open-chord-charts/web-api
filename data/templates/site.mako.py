# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1341923530.825328
_enable_loop = True
_template_filename = '/home/cbenz/dev/projets/openchordcharts/openchordcharts/templates/site.mako'
_template_uri = '/site.mako'
_source_encoding = 'utf-8'
from markupsafe import escape_silent
_exports = [u'footer', u'script', u'html_tag_opening', u'css', u'title']


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        def html_tag_opening():
            return render_html_tag_opening(context.locals_(__M_locals))
        def script():
            return render_script(context.locals_(__M_locals))
        eco_template = context.get('eco_template', UNDEFINED)
        def footer():
            return render_footer(context.locals_(__M_locals))
        request = context.get('request', UNDEFINED)
        def title():
            return render_title(context.locals_(__M_locals))
        def css():
            return render_css(context.locals_(__M_locals))
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<!DOCTYPE html>\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'html_tag_opening'):
            context['self'].html_tag_opening(**pageargs)
        

        # SOURCE LINE 4
        __M_writer(u'\n\n')
        # SOURCE LINE 26
        __M_writer(u'\n\n  <head>\n    <meta charset="utf-8">\n    <meta name="description" content="Open Chord Charts project">\n    <meta name="author" content="Christophe Benz">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1, maximum-scale=1.0, ')
        # SOURCE LINE 33
        __M_writer(u'user-scalable=0">\n    <title>')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'title'):
            context['self'].title(**pageargs)
        

        # SOURCE LINE 34
        __M_writer(u'</title>\n    ')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'css'):
            context['self'].css(**pageargs)
        

        # SOURCE LINE 48
        __M_writer(u'\n   </head>\n  <body>\n\n    ')
        # SOURCE LINE 52
        runtime._include_file(context, u'navbar.mako', _template_uri)
        __M_writer(u'\n\n    <div class="container">\n      <article>')
        # SOURCE LINE 55
        __M_writer(eco_template )
        __M_writer(u'</article>\n      <footer>\n        <hr>\n        ')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'footer'):
            context['self'].footer(**pageargs)
        

        # SOURCE LINE 58
        __M_writer(u'\n        <p>Copyright \xa9 The Open Chord Charts contributors, 2012</p>\n        <p class="application-cache-info"></p>\n        <p class="navigator-info"></p>\n      </footer>\n    </div>\n\n    ')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'script'):
            context['self'].script(**pageargs)
        

        # SOURCE LINE 89
        __M_writer(u'\n  </body>\n</html>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_footer(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def footer():
            return render_footer(context)
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_script(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        request = context.get('request', UNDEFINED)
        def script():
            return render_script(context)
        __M_writer = context.writer()
        # SOURCE LINE 65
        __M_writer(u'\n    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"></script>\n    <script src="')
        # SOURCE LINE 67
        __M_writer(escape_silent(request.static_path('openchordcharts:static/bootstrap-2.0.4/js/bootstrap{0}.js'.format(
'' if request.registry.settings['development_mode'] else '.min'))))
        # SOURCE LINE 68
        __M_writer(u'"></script>\n    <script src="')
        # SOURCE LINE 69
        __M_writer(escape_silent(request.static_path('openchordcharts:static/application.js')))
        __M_writer(u'"></script>\n    <script>\n$(function() {\n  var index = require("index");\n  var app = new index.App({\n    el: $("body")\n  });\n});\n\n')
        # SOURCE LINE 78
        if request.registry.settings['google.analytics.key']:
            # SOURCE LINE 79
            __M_writer(u"var _gaq = _gaq || [];\n_gaq.push(['_setAccount', '")
            # SOURCE LINE 80
            __M_writer(escape_silent(request.registry.settings['google.analytics.key']))
            __M_writer(u"']);\n_gaq.push(['_trackPageview']);\n(function() {\n  var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;\n  ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';\n  var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);\n})();\n")
            pass
        # SOURCE LINE 88
        __M_writer(u'    </script>\n    ')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_html_tag_opening(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def html_tag_opening():
            return render_html_tag_opening(context)
        __M_writer = context.writer()
        # SOURCE LINE 2
        __M_writer(u'\n<html>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_css(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        request = context.get('request', UNDEFINED)
        def css():
            return render_css(context)
        __M_writer = context.writer()
        # SOURCE LINE 35
        __M_writer(u'\n    <link href="')
        # SOURCE LINE 36
        __M_writer(escape_silent(request.static_path('openchordcharts:static/bootstrap-2.0.4/css/bootstrap{0}.css'.format(
'' if request.registry.settings['development_mode'] else '.min'))))
        # SOURCE LINE 37
        __M_writer(u'" rel="stylesheet">\n    <style>\n      body {\n        padding-top: 60px;\n        padding-bottom: 40px;\n      }\n    </style>\n\n    <link href="')
        # SOURCE LINE 45
        __M_writer(escape_silent(request.static_path('openchordcharts:static/bootstrap-2.0.4/css/bootstrap-responsive{0}.css'.format(
'' if request.registry.settings['development_mode'] else '.min'))))
        # SOURCE LINE 46
        __M_writer(u'" rel="stylesheet">\n    <link href="')
        # SOURCE LINE 47
        __M_writer(escape_silent(request.static_path('openchordcharts:static/application.css')))
        __M_writer(u'" rel="stylesheet">\n    ')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_title(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def title():
            return render_title(context)
        __M_writer = context.writer()
        # SOURCE LINE 34
        __M_writer(u'OpenChordCharts')
        return ''
    finally:
        context.caller_stack._pop_frame()


