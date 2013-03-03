# -*- coding: utf-8 -*-


# Open Chord Charts -- Database of free chord charts
# By: Christophe Benz <contact@openchordcharts.org>
#
# Copyright (C) 2012-2013 Christophe Benz
# https://gitorious.org/open-chord-charts/
#
# This file is part of Open Chord Charts.
#
# Open Chord Charts is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Open Chord Charts is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""Mako templates rendering functions."""


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
