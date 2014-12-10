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


from markupsafe import Markup


def get_login_url(request):
    settings = request.registry.settings
    if settings['authentication.fake_login']:
        return request.route_path('fake_login', _query=dict(callback_path=request.path_qs))
    elif settings['authentication.openid.application_name']:
        return request.route_path('openidconnect_login', _query=dict(callback_path=request.path_qs))
    elif settings['authentication.localdb_login_enabled']:
        return request.route_path('localdb_login', _query=dict(state=request.path_qs))
    else:
        return None


def iter_chords(chart, part_name):
    part_chords = chart.parts[part_name]
    previous_chord = part_chords[0]
    yield previous_chord
    for chord in part_chords[1:]:
        if chord == previous_chord:
            yield None
        else:
            yield chord
        previous_chord = chord


def iter_parts(chart):
    nb_parts_occurencies = {}
    for part_name in chart.structure:
        if part_name in nb_parts_occurencies:
            nb_parts_occurencies[part_name] += 1
        else:
            nb_parts_occurencies[part_name] = 0
        yield part_name, nb_parts_occurencies[part_name]


def render_chord(chord):
    rendered_chord = chord
    if rendered_chord.endswith('b5'):
        rendered_chord = rendered_chord[:-2] + Markup('<sup>{0}</sup>'.format(rendered_chord[-2:]))
    # FIXME This is ugly, I have to rewrite the font!
    rendered_chord = rendered_chord.replace('#', '<')
    rendered_chord = rendered_chord.replace('b', '>')
    return rendered_chord
