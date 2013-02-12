# -*- coding: utf-8 -*-


"""Mako templates rendering"""


import json
import mako.lookup
import os


js = lambda x: json.dumps(x, encoding='utf-8', ensure_ascii=False)


def load_templates(ctx):
    # Create the Mako TemplateLookup, with the default auto-escaping.
    return mako.lookup.TemplateLookup(
        default_filters=['h'],
        directories=[os.path.join(ctx.conf['app_dir'], 'templates')],
        input_encoding='utf-8',
        module_directory=os.path.join(ctx.conf['cache_dir'], 'templates'),
        )


def render(ctx, template_path, **kw):
    return ctx.templates.get_template(template_path).render_unicode(
        ctx=ctx,
        js=js,
        N_=lambda message: message,
        req=ctx.req,
        **kw
        ).strip()


def render_def(ctx, template_path, def_name, **kw):
    return ctx.templates.get_template(template_path).get_def(def_name).render_unicode(
        _=ctx.translator.ugettext,
        ctx=ctx,
        js=js,
        N_=lambda message: message,
        req=ctx.req,
        **kw
        ).strip()
