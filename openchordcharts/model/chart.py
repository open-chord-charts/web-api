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


import datetime

from biryani.baseconv import check, noop, pipe, struct
from biryani.bsonconv import object_id_to_str
from biryani.datetimeconv import datetime_to_iso8601
from biryani.objectconv import object_to_clean_dict
from biryani.strings import slugify

from suq.monpyjama import Mapper, Wrapper

from openchordcharts.model.user import User
from openchordcharts.utils import get_transposed_chord


class InvalidChartException(Exception):
    pass


class Chart(Mapper, Wrapper):
    collection_name = 'charts'

    chords = None
    compositors = None
    created_at = None
    genre = None
    key = None
    keywords = None
    modified_at = None
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
        parts = self.structure if part_name is None else [part_name]
        for part_name in parts:
            for chord in self.parts[part_name]:
                if key is None:
                    yield chord
                else:
                    yield get_transposed_chord(chord=chord, from_key=self.key, to_key=key)

    def save(self, *args, **kwargs):
        self.validate()
        return super(Chart, self).save(*args, **kwargs)

    def to_json(self):
        return check(pipe(
            object_to_clean_dict,
            struct(
                dict(
                    _id=object_id_to_str,
                    created_at=datetime_to_iso8601,
                    modified_at=datetime_to_iso8601,
                    ),
                default=noop,
                ),
            ))(self)

    def validate(self):
        if not self.title:
            raise InvalidChartException(u'Chart has no title.')
        if self.user:
            if User.find_one(dict(slug=self.user)) is None:
                raise InvalidChartException(u'Chart user does not exist.')
        else:
            raise InvalidChartException(u'Chart has no user.')
        if self.created_at is None:
            self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()
        if self.slug is None:
            self.slug = self.generate_unique_slug()
        if self.keywords is None:
            self.keywords = self.slug.split('-')
