# -*- coding: utf-8 -*-

import pymongo
from suq.monpyjama import Wrapper


db = None


def initialize_model(settings):
    database_uri = settings.get('database.uri')
    assert database_uri is not None, u'database.uri key is missing in paste ini file.'
    connection = pymongo.Connection(host=database_uri)
    database_name = database_uri.rsplit('/', 1)[1]
    global db
    db = connection[database_name]
    Wrapper.db = db
