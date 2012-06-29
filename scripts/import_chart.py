#!/usr/bin/env python
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


import argparse
import json
import sys

from pyramid.paster import bootstrap

from openchordcharts.model.chart import Chart
from openchordcharts.model.user import User


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser(description=u'Import chords chart.')
    parser.add_argument('ini_file', help=u'Paster INI configuration file')
    parser.add_argument('json_file', help=u'JSON file name')
    parser.add_argument('-c', '--create', action='store_true', help=u'Create user if it does not exist')
    parser.add_argument('-u', '--user', help=u'Set user name chart')
    arguments = parser.parse_args(args)

    env = bootstrap(arguments.ini_file)

    with open(arguments.json_file) as f:
        chart_str = f.read()
    chart_bson = json.loads(chart_str)
    chart = Chart.from_bson(chart_bson)
    if arguments.user:
        chart.user = arguments.user
    user = User.find_one(dict(slug=chart.user))
    if user is None:
        if arguments.create:
            user = User()
            user.slug = chart.user
            user.save(safe=True)
        else:
            print u'Chart user does not exist.'.encode('utf-8')
    if user:
        chart_id = chart.save(safe=True)
        print unicode(chart_id).encode('utf-8')

    return 0


if __name__ == '__main__':
    sys.exit(main())
