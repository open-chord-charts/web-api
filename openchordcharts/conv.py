# -*- coding: utf-8 -*-


# Open Chord Charts -- Database of free chord charts
# By: Christophe Benz <christophe.benz@gmail.com>
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


from biryani1.baseconv import check, cleanup_line, function, noop, pipe, set_value, struct, test_in
from biryani1.datetimeconv import datetime_to_iso8601_str
from biryani1.objectconv import object_to_clean_dict
import biryani1.states

from .helpers import music_theory


# State

default_state = biryani1.states.default_state


# Level 1 converters

chart_to_json_dict = check(
    pipe(
        object_to_clean_dict,
        struct(
            {
                '_id': set_value(None),
                'created_at': datetime_to_iso8601_str,
                'keywords': set_value(None),
                'modified_at': datetime_to_iso8601_str,
                },
            default=noop,
            drop_none_values=True,
            ),
        )
    )

input_to_chart_key = pipe(
    cleanup_line,
    function(lambda value: value.lower()),
    test_in([key.lower() for key in music_theory.iter_chromatic_keys()]),
    function(lambda value: value.capitalize()),
    )

params_to_chart_index_data = struct(
    {
        'q': cleanup_line,
        },
    default=noop,
    drop_none_values=False,
    )


# Level 2 converters

params_to_chart_view_data = struct(
    {
        'key': pipe(cleanup_line, input_to_chart_key),
        },
    default=noop,
    drop_none_values=False,
    )
