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
import logging
import os
import sys

from paste.deploy import loadapp

from openchordcharts.model.chart import Chart
from openchordcharts.model.user import User


log = logging.getLogger(os.path.basename(__file__))


def import_chart(json_filename, user_slug, create=False):
    with open(json_filename) as f:
        json_str = f.read()
    json_charts = json.loads(json_str)
    if isinstance(json_charts, dict):
        json_charts = [json_charts]

    for json_chart in json_charts:
        chart = Chart()
        chart.update_from_dict(dict(
            (key, value)
            for key, value in json_chart.iteritems()
            if key not in ['_id', 'created_at', 'keywords', 'modified_at', 'slug']
            ))
        if user_slug:
            chart.user_slug = user_slug
        user = User.find_one(dict(slug=chart.user_slug))
        if user_slug:
            chart_id = chart.save(safe=True)
            log.debug(chart_id)
        else:
            if create:
                user = User()
                user.slug = chart.user_slug
                user.save(safe=True)
            else:
                log.error(u'Chart user does not exist (title={0}).'.format(chart.title))


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser(description=u'Import chords chart.')
    parser.add_argument('ini_filename', help=u'Paster INI configuration file')
    parser.add_argument('json_filename', help=u'JSON file name. File can contain an object or a list of objects.')
    parser.add_argument('-c', '--create', action='store_true', help=u'Create user if it does not exist')
    parser.add_argument('-u', '--user-slug', help=u'Set chart user slug')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help=u'Display info messages')
    arguments = parser.parse_args(args)
    logging.basicConfig(level=logging.DEBUG if arguments.verbose else logging.WARNING)
    loadapp(u'config:{0}#main'.format(os.path.abspath(arguments.ini_filename)))
    import_chart(
        create=arguments.create,
        json_filename=arguments.json_filename,
        user_slug=arguments.user_slug,
        )
    return 0


if __name__ == '__main__':
    sys.exit(main())
