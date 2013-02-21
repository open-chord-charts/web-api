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
from openchordcharts.model.account import Account


log = logging.getLogger(os.path.basename(__file__))


def import_charts(ctx, json_filename, user_id=None):
    account = None
    if user_id is not None:
        accounts_cursor = Account.find({
            'user_id': user_id,
            })
        if accounts_cursor.count() == 0:
            log.error(u'user_id "{0}" not found in accounts collection'.format(user_id))
            return None
        elif accounts_cursor.count() > 1:
            log.error(u'user_id "{0}" corresponds to many accounts'.format(user_id))
            return None
        account = accounts_cursor.next()
    with open(json_filename) as _file:
        json_str = _file.read()
    json_charts = json.loads(json_str)
    if isinstance(json_charts, dict):
        json_charts = [json_charts]
    for json_chart in json_charts:
        chart = Chart()
        for key in ['composers', 'genre', 'key', 'parts', 'structure', 'title']:
            setattr(chart, key, json_chart.get(key))
        if account is not None:
            chart.account_id = account._id
        chart_id = chart.save(safe=True)
        log.debug(chart_id)
    return None


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser(description=u'Import chords chart.')
    parser.add_argument('ini_filename', help=u'Paster INI configuration file')
    parser.add_argument('json_filename', help=u'JSON file name. File can contain an object or a list of objects.')
    parser.add_argument('-u', '--user-id', help=u'Set chart owner user ID')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help=u'Display info messages')
    arguments = parser.parse_args(args)
    logging.basicConfig(level=logging.DEBUG if arguments.verbose else logging.WARNING)
    app = loadapp(u'config:{0}#main'.format(os.path.abspath(arguments.ini_filename)))
    import_charts(
        ctx=app.ctx,
        json_filename=arguments.json_filename,
        user_id=arguments.user_id,
        )
    return 0


if __name__ == '__main__':
    sys.exit(main())
