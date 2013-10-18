# -*- coding: utf-8 -*-


# Open Chord Charts -- Database of free chord charts
# By: Christophe Benz <contact@openchordcharts.org>
#
# Copyright (C) 2012-2013 Christophe Benz
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


"""Database loading functions."""


import pymongo
import suq.monpyjama


class Wrapper(suq.monpyjama.Wrapper):
    pass


def ensure_indexes(ctx):
    ctx.db.accounts.ensure_index([('slug', pymongo.ASCENDING)], unique=True)
    ctx.db.charts.ensure_index([('account_id', pymongo.ASCENDING)])
    ctx.db.charts.ensure_index([('keywords', pymongo.ASCENDING)])
    ctx.db.charts.ensure_index([('slug', pymongo.ASCENDING)])
    ctx.db.charts.ensure_index([('account_id', pymongo.ASCENDING), ('slug', pymongo.ASCENDING)], unique=True)
    ctx.db.charts.ensure_index([('title', pymongo.ASCENDING)])


def load_database(ctx):
    connection = pymongo.Connection(host=ctx.conf['database.host_name'], port=ctx.conf['database.port'])
    db = connection[ctx.conf['database.name']]
    Wrapper.db = db
    return db
