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
import re

from biryani.baseconv import check
from biryani.objectconv import object_to_clean_dict
from biryani.strings import slugify
from suq.monpyjama import Mapper, Wrapper

from openchordcharts.utils import get_transposed_chord


class Chart(Mapper, Wrapper):
    collection_name = 'charts'
    composers = None
    created_at = None
    genre = None
    is_deleted = None
    keywords = None
    modified_at = None
    key = None
    parts = None
    slug = None
    structure = None
    title = None
    user = None

    def compute_keywords(self):
        keywords = []
        keywords.extend(self.slug.split('-'))
        if self.composers:
            keywords.extend(slugify(' '.join(self.composers)).split('-'))
        return keywords

    def equals(self, other_dict):
        ignored_attributes = ['_id', 'created_at', 'is_deleted', 'keywords', 'modified_at', 'slug', 'user']
        return dict((key, value) for key, value in other_dict.iteritems() if key not in ignored_attributes) == \
            dict(
                (key, value)
                for key, value in check(object_to_clean_dict(self)).iteritems()
                if key not in ignored_attributes
                )

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

    @classmethod
    def get_search_by_keywords_spec(cls, keywords):
        keywords_regexps = [re.compile(u'^{0}'.format(re.escape(keyword))) for keyword in keywords]
        return {'$all': keywords_regexps}

    def iter_chords(self, to_key=None, part_name=None):
        parts = self.structure if part_name is None else [part_name]
        for part_name in parts:
            for chord in self.parts[part_name]:
                if to_key is None:
                    yield chord
                else:
                    yield get_transposed_chord(chord=chord, from_key=self.key, to_key=to_key)

    def save(self, *args, **kwargs):
        if self.created_at is None:
            self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()
        return super(Chart, self).save(*args, **kwargs)

    def to_bson(self):
        if self.slug is None or self.slug != slugify(self.title):
            self.slug = self.generate_unique_slug()
        self.keywords = self.compute_keywords()
        return check(object_to_clean_dict(self))

    def transpose(self, to_key):
        for part_name in self.parts:
            self.parts[part_name] = list(self.iter_chords(part_name=part_name, to_key=to_key))
        self.key = to_key

    def update_from_dict(self, data):
        for k, v in data.iteritems():
            setattr(self, k, v)


class HistoryChart(Chart):
    chart_id = None
    collection_name = 'history_charts'

    def save(self, *args, **kwargs):
        self.keywords = None
        self.slug = None
        return super(Chart, self).save(*args, **kwargs)

    def to_bson(self):
        return check(object_to_clean_dict(self))
