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

from openchordcharts.model.openidconnect import Authentication, Client, Provider


db = None


def initialize_model(settings):
    database_uri = settings.get('database.uri')
    assert database_uri is not None, u'database.uri key is missing in paste ini file.'
    connection = pymongo.Connection(host=database_uri)
    database_name = database_uri.rsplit('/', 1)[1]
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

    # OpenID Connect providers collection
    Provider.ensure_index('expiration', sparse=True)
    Provider.ensure_index('url')

    wannanou.init(Authentication=Authentication, Client=Client, Provider=Provider, RequestFile=None)
