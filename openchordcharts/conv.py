# -*- coding: utf-8 -*-


# Open Chord Charts -- Database of free chord charts
# By: Christophe Benz <christophe.benz@gmail.com>
#
# Copyright (C) 2012 Christophe Benz
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


from biryani.baseconv import (check, cleanup_line, default, function, guess_bool, input_to_email, input_to_int,
    make_input_to_url, noop, not_none, pipe, set_value, struct, test, test_in, uniform_mapping, uniform_sequence)
from biryani.bsonconv import input_to_object_id
from biryani.datetimeconv import datetime_to_iso8601_str
from biryani.objectconv import object_to_clean_dict
import biryani.states

from openchordcharts.utils import iter_chromatic_keys


# State

default_state = biryani.states.default_state


# Converters

chart_to_json_dict = check(
    pipe(
        object_to_clean_dict,
        struct(
            dict(
                _id=set_value(None),
                chart_id=set_value(None),
                created_at=datetime_to_iso8601_str,
                keywords=set_value(None),
                modified_at=datetime_to_iso8601_str,
                ),
            default=noop,
            ),
        )
    )

csv_input_to_list = pipe(
    function(lambda value: value.split(',')),
    uniform_sequence(cleanup_line),
    )

input_to_key = pipe(
    cleanup_line,
    function(lambda s: s.lower()),
    test_in([key.lower() for key in iter_chromatic_keys()]),
    function(lambda s: s.capitalize()),
    )

params_to_charts_data = struct(
    dict(
        include_deleted=guess_bool,
        q=cleanup_line,
        ),
    default=noop,
    keep_none_values=True,
    )

params_to_charts_json_data = struct(
    dict(
        include_deleted=guess_bool,
        q=cleanup_line,
        slug=cleanup_line,
        title=cleanup_line,
        user=cleanup_line,
        ),
    default=noop,
    keep_none_values=True,
    )

params_to_chart_data = struct(
    dict(
        key=pipe(cleanup_line, input_to_key),
        revision=pipe(cleanup_line, input_to_object_id),
        ),
    default=noop,
    keep_none_values=True,
    )

params_to_index_data = struct(
    dict(
        appcache=pipe(guess_bool, default(True)),
        ),
    default=noop,
    keep_none_values=True,
    )

validate_settings = check(
        pipe(
            struct(
                {
                    'authentication.fake_login': pipe(cleanup_line, input_to_email),
                    'authentication.openid.application_name': cleanup_line,
                    'authentication.openid.client_id': cleanup_line,
                    'authentication.openid.client_secret': cleanup_line,
                    'authentication.openid.provider_url': pipe(cleanup_line, make_input_to_url()),
                    'authentication.secret': pipe(cleanup_line, not_none),
                    'charts.limit': input_to_int,
                    'css.bootstrap': cleanup_line,
                    'css.bootstrap_responsive': cleanup_line,
                    'database.uri': pipe(cleanup_line, not_none),
                    'development_mode': guess_bool,
                    'google.analytics.key': cleanup_line,
                    'javascript.bootstrap': cleanup_line,
                    'javascript.jquery': cleanup_line,
                    'javascript.spinejs_dir': cleanup_line,
                    },
                default=noop,
                keep_none_values=True,
                ),
            test(lambda values: len(filter(None, [value for key, value in values.iteritems() if key in [
                    'authentication.openid.application_name',
                    'authentication.openid.client_id',
                    'authentication.openid.client_secret',
                    'authentication.openid.provider_url',
                    ]])) in [0, 4], default_state._(u'Not all authentication.openid keys are set')
                ),
            )
        )


def params_to_chart_edit_data(params, state=default_state):
    all_errors = {}
    value, error = struct(
        dict(
            composers=csv_input_to_list,
            genre=cleanup_line,
            key=input_to_key,
            parts=uniform_mapping(
                cleanup_line,
                pipe(
                    function(lambda value: value.split()),
                    uniform_sequence(cleanup_line),
                    ),
                ),
            structure=pipe(
                csv_input_to_list,
                uniform_sequence(
                    function(lambda value: value.upper()),
                    ),
                ),
            title=pipe(
                cleanup_line,
                not_none,
                ),
            ),
        default=noop,
        keep_none_values=True,
        )(params)
    if error is not None:
        all_errors.update(error)
    if value is None:
        return None, all_errors or None
    if value['structure'] is not None:
        if value['parts'] is None:
            value['parts'] = dict()
        for part_name in value['structure']:
            value['parts'].setdefault(part_name, [])
            part_value, error = test(lambda value: len(value) > 0, error=state._(u'Missing value'))(
                value['parts'][part_name])
            if error is not None:
                all_errors.update({'parts.{0}'.format(part_name): error})
    return value, all_errors or None
