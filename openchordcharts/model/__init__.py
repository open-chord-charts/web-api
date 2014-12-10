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


import pymongo
from suq.monpyjama import Wrapper
import wannanou

from openchordcharts.model.chart import Chart
from openchordcharts.model.openidconnect import Authentication, Client, Provider
from openchordcharts.model.user import User


db = None


def initialize_model(settings):
    connection = pymongo.Connection(host=settings['database.uri'])
    database_name = settings['database.uri'].rsplit('/', 1)[1]
    global db
    db = connection[database_name]
    Wrapper.db = db

    # OpenID Connect authentications collection
    Authentication.ensure_index('expiration')
    Authentication.ensure_index([
        ('provider_url', pymongo.ASCENDING),
        ('grant_type', pymongo.ASCENDING),
        ('scope', pymongo.ASCENDING),
        ])
    Authentication.ensure_index('state', sparse=True, unique=True)

    Chart.ensure_index('is_deleted')
    Chart.ensure_index('keywords')
    Chart.ensure_index('slug')
    Chart.ensure_index('title')
    Chart.ensure_index('user')

    # OpenID Connect providers collection
    Provider.ensure_index('expiration', sparse=True)
    Provider.ensure_index('url')

    User.ensure_index('email')
    User.ensure_index('slug')

    wannanou.init(Authentication=Authentication, Client=Client, Provider=Provider, RequestFile=None)
