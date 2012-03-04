# -*- coding: utf-8 -*-

from markupsafe import Markup


def render_chord(chord):
    rendered_chord = chord
    if rendered_chord.endswith('b5'):
        rendered_chord = rendered_chord[:-2] + Markup('<sup>{0}</sup>'.format(rendered_chord[-2:]))
    return rendered_chord
