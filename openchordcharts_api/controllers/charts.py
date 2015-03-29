# -*- coding: utf-8 -*-


# Open Chord Charts -- Database of free chord charts
# By: Christophe Benz <contact@openchordcharts.org>
#
# Copyright (C) 2012 Christophe Benz
# https://github.com/openchordcharts/
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


"""Charts controller functions."""


import re

import webob
from webob.dec import wsgify

from .. import conf, contexts, conv, model, urls, wsgihelpers


# Routes

def route_api1(environ, start_response):
    req = webob.Request(environ)
    ctx = contexts.Ctx(req)

    chart, error = conv.pipe(
        conv.input_to_slug,
        conv.not_none,
        model.Chart.make_id_or_slug_to_instance(),
        )(req.urlvars.get('id_or_slug'), state=ctx)
    if error is not None:
        return wsgihelpers.not_found(ctx, message=error)(environ, start_response)

    ctx.node = chart

    router = urls.make_router(
        ('GET', '^$', api1_view),
        ('POST', '^$', api1_create_or_edit),
        (('GET', 'POST'), '^/delete$', api1_delete),
        )
    return router(environ, start_response)


def route_api1_class(environ, start_response):
    router = urls.make_router(
        ('GET', '^$', api1_search),
        ('POST', '^$', api1_create_or_edit),
        (None, '^/(?P<id_or_slug>[^/]+)(?=/|$)', route_api1),
        )
    return router(environ, start_response)


# Controllers

@wsgify
def api1_create_or_edit(req):
    ctx = contexts.Ctx(req)
    user = model.get_user(ctx, check=True)
    is_create_mode = ctx.node is None
    chart_attributes, errors = conv.pipe(
        conv.input_to_json_dict,
        conv.struct(
            {
                'composers': conv.validate_list_of_strings,
                'compositionYear': conv.test_isinstance(int),
                'genre': conv.pipe(
                    conv.test_isinstance(unicode),
                    conv.cleanup_line,
                    ),
                'interpretations': conv.pipe(
                    conv.test_isinstance(list),
                    conv.uniform_sequence(
                        conv.pipe(
                            conv.test_isinstance(dict),
                            conv.struct(
                                {
                                    'externalLinks': conv.pipe(
                                        conv.test_isinstance(list),
                                        conv.uniform_sequence(
                                            conv.pipe(
                                                conv.test_isinstance(unicode),
                                                conv.make_str_to_url(full=True),
                                                conv.not_none,
                                                ),
                                            ),
                                        ),
                                    'interpreterName': conv.empty_to_none,
                                    'year': conv.test_isinstance(int),
                                    },
                                default=None,  # Fail if unexpected item.
                                ),
                            conv.empty_to_none,
                            conv.not_none,
                            ),
                        ),
                    conv.empty_to_none,
                    ),
                'key': conv.pipe(
                    conv.test_isinstance(unicode),
                    conv.cleanup_line,
                    conv.str_to_chart_key,
                    conv.not_none,
                    ),
                'parts': conv.pipe(
                    conv.test_isinstance(dict),
                    conv.uniform_mapping(
                        conv.cleanup_line,
                        conv.pipe(
                            conv.test_isinstance(list),
                            conv.uniform_sequence(
                                conv.pipe(
                                    conv.test_isinstance(dict),
                                    conv.struct(
                                        {
                                            'alterations': conv.pipe(
                                                conv.test_isinstance(list),
                                                conv.uniform_sequence(
                                                    conv.pipe(
                                                        conv.test_isinstance(unicode),
                                                        conv.empty_to_none,
                                                        conv.not_none,
                                                        ),
                                                    ),
                                                ),
                                            'degree': conv.pipe(
                                                conv.test_isinstance(int),
                                                conv.test_between(0, 11),
                                                ),
                                            'duration': conv.anything_to_float,
                                            },
                                        default=None,  # Fail if unexpected item.
                                        ),
                                    conv.empty_to_none,
                                    conv.not_none,
                                    ),
                                ),
                            ),
                        ),
                    ),
                'structure': conv.validate_list_of_strings,
                'title': conv.pipe(
                    conv.test_isinstance(unicode),
                    conv.cleanup_line,
                    conv.not_none,
                    ),
                },
            default=None,  # Fail if unexpected item.
            ),
        conv.validate_structure_and_parts,
        )(req.body, state=ctx)
    if errors is not None:
        return wsgihelpers.bad_request(ctx, errors=errors, message=ctx._(u'Invalid JSON'))
    chart_already_exists = lambda ctx, slug: \
        wsgihelpers.bad_request(ctx, message=ctx._(u'Chart with slug "{}" already exists'.format(slug)))
    if is_create_mode:
        slug = conv.slugify(chart_attributes['title'])
        existing_chart = model.Chart.find_one({'slug': slug})
        if existing_chart is not None:
            return chart_already_exists(ctx, slug)
        chart_attributes['owner_account_id'] = user._id
        chart = model.Chart(**chart_attributes)
    else:
        chart = ctx.node
        model.check_owner(ctx, user, chart)
        slug = conv.slugify(chart_attributes['title'])
        existing_chart = model.Chart.find_one({'_id': {'$ne': chart._id}, 'slug': slug})
        if existing_chart is not None:
            return chart_already_exists(ctx, slug)
        chart.set_attributes(**chart_attributes)
    chart.compute_attributes()
    chart.save(safe=True)
    return wsgihelpers.respond_json(ctx, {'chart': chart.to_json(state=ctx)})


@wsgify
def api1_delete(req):
    ctx = contexts.Ctx(req)
    user = model.get_user(ctx, check=True)
    chart = ctx.node
    model.check_owner(ctx, user, chart)
    chart.delete(safe=True)
    return wsgihelpers.respond_json(ctx, {'delete': 'ok'})


@wsgify
def api1_search(req):
    ctx = contexts.Ctx(req)
    data, errors = conv.struct(
        {
            'ownerSlug': conv.cleanup_line,
            'q': conv.cleanup_line,
            },
        default=None,  # Fail if unexpected item.
        )(req.params, state=conv.default_state)
    if errors is not None:
        return wsgihelpers.bad_request(ctx, errors=errors)
    spec = {}
    keywords = None
    if data['q'] is not None:
        keywords = data['q'].strip().split()
        spec['keywords'] = {'$all': [re.compile(u'^{0}'.format(re.escape(keyword))) for keyword in keywords]}
    if data['ownerSlug']:
        owner_account = model.Account.find_one({'username': data['ownerSlug']})
        if owner_account is None:
            return wsgihelpers.bad_request(ctx, message=ctx._(u'Invalid account: {}'.format(data['ownerSlug'])))
        spec['owner_account_id'] = owner_account._id
    charts_cursor = model.Chart.find(spec).sort('slug').limit(conf['charts.limit'])
    return wsgihelpers.respond_json(ctx, {
        'charts': [chart.to_json(state=ctx, with_owner=True) for chart in charts_cursor],
    })


@wsgify
def api1_view(req):
    ctx = contexts.Ctx(req)
    chart = ctx.node
    return wsgihelpers.respond_json(ctx, {'chart': chart.to_json(state=ctx, with_owner=True)})
