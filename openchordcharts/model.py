# -*- coding: utf-8 -*-

from suq.monpyjama import Mapper, Wrapper
import pymongo


db = None


def add_request_attributes(event):
    global db
    request = event.request
    request.db = db


def initialize_model(settings):
    database_uri = settings.get('database.uri')
    assert database_uri is not None, u'database.uri key is missing in paste ini file.'
    connection = pymongo.Connection(host=database_uri)
    database_name = database_uri.rsplit('/', 1)[1]
    global db
    db = connection[database_name]
    Wrapper.db = db


class Chart(Mapper, Wrapper):
    collection_name = 'charts'

    chords = None
    compositors = None
    genre = None
    key = None
    parts = None
    slug = None
    structure = None
    title = None
    user = None

    def get_part_chords(self, part):
        index = 0
        for current_part in self.structure:
            count = self.parts[current_part]['count']
            if current_part == part:
                return self.chords[index:index + count]
            else:
                index += count
        return None
