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


import itertools
import re

from biryani1.baseconv import (cleanup_line, function, noop, not_none, pipe, set_value, struct, test_in,
    uniform_mapping, uniform_sequence)
from biryani1.datetimeconv import datetime_to_iso8601_str
from biryani1.objectconv import object_to_clean_dict
import biryani1.states

from . import chart_render, music_theory


# State

default_state = biryani1.states.default_state


# Level 1 converters

chart_to_inputs = pipe(
    object_to_clean_dict,
    struct(
        {
            '_id': set_value(None),
            'account_id': set_value(None),
            'composers': function(lambda value: ', '.join(value)),
            'created_at': datetime_to_iso8601_str,
            'is_deleted': set_value(None),
            'keywords': set_value(None),
            'modified_at': datetime_to_iso8601_str,
            'parts': uniform_mapping(
                noop,
                function(lambda values: '\n'.join(' '.join(row) for row in chart_render.grouper(8, values, ''))),
                ),
            'slug': set_value(None),
            'structure': function(lambda value: ', '.join(value)),
            },
        default=noop,
        drop_none_values=True,
        ),
    )

chart_to_json_dict = pipe(
    object_to_clean_dict,
    struct(
        {
            '_id': set_value(None),
            'account_id': set_value(None),
            'created_at': datetime_to_iso8601_str,
            'is_deleted': set_value(None),
            'keywords': set_value(None),
            'modified_at': datetime_to_iso8601_str,
            },
        default=noop,
        drop_none_values=True,
        ),
    )

params_to_chart_index_data = struct(
    {
        'q': cleanup_line,
        },
    default=noop,
    drop_none_values=False,
    )

str_csv_to_list = pipe(
    function(lambda value: value.split(',')),
    uniform_sequence(cleanup_line),
    function(lambda values: [value for value in values if value is not None]),
    )

str_to_chart_key = pipe(
    function(lambda value: value.capitalize()),
    test_in(list(itertools.chain.from_iterable(music_theory.chromatic_keys))),
    )


def str_to_chord_dict(value, state=None):
    if value is None:
        return None, None
    original_value = value
    value = value.strip().capitalize()
    match = re.match(music_theory.chord_regex, value)
    if match is None:
        return original_value, u'Invalid value'
    value = match.groupdict()
    value['key'] = value['key'].strip() or None
    value['quality'] = value['quality'].strip() or None
    if value['quality'] is not None and value['quality'] not in music_theory.chord_qualities:
        return original_value, u'Invalid value'
    return value, None


# Level 2 converters

inputs_to_chart_edit_data = struct(
    {
        'composers': pipe(cleanup_line, str_csv_to_list),
        'genre': cleanup_line,
        'key': pipe(cleanup_line, str_to_chart_key, not_none),
        'parts': uniform_mapping(
            cleanup_line,
            pipe(
                function(lambda value: value.split()),
                uniform_sequence(
                    pipe(
                        cleanup_line,
                        str_to_chord_dict,
                        function(lambda value: u'{0}{1}'.format(value['key'], value['quality'] or '')),
                        ),
                    ),
                ),
            ),
        'structure': pipe(
            cleanup_line,
            str_csv_to_list,
            uniform_sequence(
                function(lambda value: value.upper()),
                ),
            ),
        'title': pipe(
            cleanup_line,
            not_none,
            ),
        },
    default=noop,
    drop_none_values=False,
    )

params_to_chart_view_data = struct(
    {
        'key': pipe(cleanup_line, str_to_chart_key),
        },
    default=noop,
    drop_none_values=False,
    )
