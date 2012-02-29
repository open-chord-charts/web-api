# -*- coding: utf-8 -*-

from biryani.strings import slugify
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

    def generate_unique_slug(self):
        title_slug = slugify(self.title)
        slug = title_slug
        slug_index = 1
        while True:
            if Chart.find_one(dict(slug=slug)) is None:
                return slug
            else:
                slug = u'{0}-{1}'.format(title_slug, slug_index)
                slug_index += 1

    def get_part_chords(self, part):
        index = 0
        for current_part in self.structure:
            count = self.parts[current_part]['count']
            if current_part == part:
                return self.chords[index:index + count]
            else:
                index += count
        return None

    def save(self, *args, **kwargs):
        self.slug = self.generate_unique_slug()
        return super(Chart, self).save(*args, **kwargs)
