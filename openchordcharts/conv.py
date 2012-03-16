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


from biryani.baseconv import *

from openchordcharts.utils import iter_chromatic_keys


csv_str_to_list = pipe(
    function(lambda value: value.split(',')),
    uniform_sequence(cleanup_line),
    )

str_to_key = pipe(
    cleanup_line,
    function(lambda s: s.lower()),
    test_in([key.lower() for key in iter_chromatic_keys()]),
    function(lambda s: s.capitalize()),
    )


def params_to_chart_data(params):
    all_errors = {}
    value, error = struct(
        dict(
            composers=csv_str_to_list,
            genre=cleanup_line,
            key=str_to_key,
            parts=uniform_mapping(
                cleanup_line,
                pipe(
                    function(lambda value: value.split()),
                    uniform_sequence(cleanup_line),
                    ),
                ),
            structure=pipe(
                csv_str_to_list,
                uniform_sequence(
                    function(lambda value: value.upper()),
                    ),
                ),
            title=pipe(
                cleanup_line,
                exists,
                ),
            ),
        default='ignore',
        keep_missing_values=True,
        )(params)
    if error is not None:
        all_errors.update(error)
    for part_name in value['structure']:
        value['parts'].setdefault(part_name, [])
        part_value, error = test(lambda value: len(value) > 0, error=u'Missing value')(value['parts'][part_name])
        if error is not None:
            all_errors.update({'parts.{0}'.format(part_name): error})
    return value, all_errors or None
