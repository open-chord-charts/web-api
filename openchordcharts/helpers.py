# -*- coding: utf-8 -*-

from markupsafe import Markup


def iter_chords(chart, part_name):
    previous_chord = chart.parts[part_name][0]
    yield previous_chord
    for chord in chart.parts[part_name][1:]:
        if chord == previous_chord:
            yield None
        else:
            yield chord
        previous_chord = chord


def iter_structure(chart):
    nb_parts_occurencies = {}
    for part_name in chart.structure:
        if part_name in nb_parts_occurencies:
            nb_parts_occurencies[part_name] += 1
        else:
            nb_parts_occurencies[part_name] = 0
        yield part_name, nb_parts_occurencies[part_name]


def render_chord(chord):
    rendered_chord = chord
    rendered_chord = rendered_chord.replace('#', '<')
    rendered_chord = rendered_chord.replace('b', '>')
    if rendered_chord.endswith('b5'):
        rendered_chord = rendered_chord[:-2] + Markup('<sup>{0}</sup>'.format(rendered_chord[-2:]))
    return rendered_chord
