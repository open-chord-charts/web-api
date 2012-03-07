#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import sys

from pyramid.paster import bootstrap

from openchordcharts.model import initialize_model
from openchordcharts.model.chart import Chart
from openchordcharts.model.user import User


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser(description=u'Import chords chart.')
    parser.add_argument('ini_file', help=u'Paster INI configuration file')
    parser.add_argument('json', help=u'JSON file name')
    parser.add_argument('-c', '--create', action='store_true', help=u'Create user if it does not exist')
    parser.add_argument('-u', '--user', help=u'Set user name chart')
    arguments = parser.parse_args(args)

    env = bootstrap(arguments.ini_file)
    settings = env['registry'].settings

    initialize_model(settings)

    with open(arguments.json) as f:
        chart_str = f.read()
    chart_json = json.loads(chart_str)
    chart = Chart.from_bson(chart_json)
    if arguments.user:
        chart.user = arguments.user
    if arguments.create and User.find_one(dict(slug=chart.user)) is None:
        user = User()
        user.slug = chart.user
        user.save(safe=True)
    chart_id = chart.save(safe=True)
    print unicode(chart_id).encode('utf-8')

    return 0


if __name__ == '__main__':
    sys.exit(main())
