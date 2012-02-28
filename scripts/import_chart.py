#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import sys

from biryani.strings import slugify
from pyramid.paster import bootstrap

from openchordcharts import model


def generate_unique_slug(title):
    title_slug = slugify(title)
    slug = title_slug
    slug_index = 1
    while True:
        if model.db.charts.find_one(dict(slug=slug)) is None:
            return slug
        else:
            slug = u'{0}-{1}'.format(title_slug, slug_index)
            slug_index += 1


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser(description=u'Import chords chart.')
    parser.add_argument('ini_file', help=u'Paster INI configuration file')
    parser.add_argument('json', help=u'JSON file name')
    arguments = parser.parse_args(args)

    env = bootstrap(arguments.ini_file)
    settings = env['registry'].settings

    model.initialize_model(settings)

    with open(arguments.json) as f:
        chart_str = f.read()
    chart = json.loads(chart_str)
    assert chart.get('title'), u'Chart must have a title.'
    chart['slug'] = generate_unique_slug(chart['title'])
    chart_db_object_id = model.db.charts.save(chart, safe=True)
    print unicode(chart_db_object_id).encode('utf-8')

    return 0


if __name__ == '__main__':
    sys.exit(main())
