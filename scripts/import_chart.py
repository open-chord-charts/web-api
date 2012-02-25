#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import os
import sys

from pyramid.paster import bootstrap

from openchordcharts import model


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
    chart_db_object_id = model.db.charts.save(chart, safe=True)
    print unicode(chart_db_object_id).encode('utf-8')

    return 0


if __name__ == '__main__':
    sys.exit(main())
