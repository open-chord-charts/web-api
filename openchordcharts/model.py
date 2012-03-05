# -*- coding: utf-8 -*-

from biryani.baseconv import check, noop, pipe, struct
from biryani.bsonconv import object_id_to_str
from biryani.objectconv import object_to_clean_dict
from biryani.strings import slugify
import pymongo
from suq.monpyjama import Mapper, Wrapper

from openchordcharts.utils import get_key_offset, get_transposed_chord


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
    keywords = None
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

    def iter_chords(self, key=None, part_name=None):
        if key is not None:
            key_offset_delta = get_key_offset(key) - get_key_offset(self.key)
        parts = self.structure if part_name is None else [part_name]
        for part_name in parts:
            for chord in self.parts[part_name]:
                if key is None:
                    yield chord
                else:
                    yield get_transposed_chord(chord, key_offset_delta)

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = self.generate_unique_slug()
        if self.keywords is None:
            self.keywords = self.slug.split('-')
        return super(Chart, self).save(*args, **kwargs)

    def to_json(self):
        return check(pipe(
            object_to_clean_dict,
            struct(
                dict(
                    _id=object_id_to_str,
                    ),
                default=noop,
                ),
            ))(self)
