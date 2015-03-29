# -*- coding: utf-8 -*-


# Open Chord Charts -- Database of free chord charts
# By: Christophe Benz <contact@openchordcharts.org>
#
# Copyright (C) 2012, 2013, 2014, 2015 Christophe Benz
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


"""Data converters."""


import collections

from biryani.baseconv import *  # NOQA
from biryani.bsonconv import *  # NOQA
from biryani.jsonconv import *  # NOQA
from biryani.objectconv import *  # NOQA
from biryani.states import default_state  # NOQA
from biryani.strings import *  # NOQA


# Level 0 converters

def debug(value, state=None):
    from pprint import pprint
    pprint(value)
    return value, None


# Level 1 converters

input_to_json_dict = pipe(
    make_input_to_json(object_pairs_hook=collections.OrderedDict),
    test_isinstance(dict),
    not_none,
    )


def method(method_name, *args, **kwargs):
    def method_converter(value, state=None):
        if value is None:
            return value, None
        return getattr(value, method_name)(state or default_state, *args, **kwargs)
    return method_converter


str_to_chart_key = pipe(
    function(lambda value: value.capitalize()),
    # test_in(list(itertools.chain.from_iterable(music_theory.chromatic_keys))),
    )


def str_to_chord_dict(value, state=None):
    if value is None:
        return None, None
    original_value = value
    value = value.strip().capitalize()
    return value, None
    # match = re.match(music_theory.chord_regex, value)
    match = None  # TODO
    if match is None:
        return original_value, u'Invalid value'
    value = match.groupdict()
    value['key'] = value['key'].strip() or None
    value['quality'] = value['quality'].strip() or None
    # if value['quality'] is not None and value['quality'] not in music_theory.chord_qualities:
    #     return original_value, u'Invalid value'
    return value, None


validate_list_of_strings = pipe(
    test_isinstance(list),
    uniform_sequence(
        pipe(
            test_isinstance(unicode),
            cleanup_line,
            not_none,
            ),
        ),
    )


def validate_structure_and_parts(values, state=None):
    if values is None:
        return values, None
    structure = values.get('structure')
    parts = values.get('parts')
    if structure is not None and parts is not None:
        for part_name in structure:
            if part_name not in parts:
                return values, state._(u'Part "{}" is declared in "structure" but is missing from "parts".'.format(
                    part_name))
    elif structure is not None or parts is not None:
        return values, state._(u'Both "structure" and "parts" must be provided, or none.')
    return values, None
