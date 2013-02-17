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

from biryani1.baseconv import check
from biryani1.objectconv import object_to_clean_dict
from biryani1.strings import slugify
from suq.monpyjama import Mapper, Wrapper


common_chromatic_keys = ['Ab', 'A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G']


class Chart(Mapper, Wrapper):
    collection_name = 'charts'
    composers = None
    created_at = None
    genre = None
    keywords = None
    modified_at = None
    key = None
    parts = None
    slug = None
    structure = None
    title = None
    user_slug = None

    def compute_keywords(self):
        keywords = []
        keywords.extend(self.slug.split('-'))
        if self.composers:
            keywords.extend(slugify(' '.join(self.composers)).split('-'))
        return keywords

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

    def has_same_data_than(self, other_dict):
        ignored_attributes = ['_id', 'created_at', 'keywords', 'modified_at', 'slug', 'user_slug']
        clean_dict = dict(
            (key, value)
            for key, value in check(object_to_clean_dict(self)).iteritems()
            if key not in ignored_attributes
            )
        clean_other_dict = dict(
            (key, value)
            for key, value in other_dict.iteritems()
            if key not in ignored_attributes
            )
        return clean_dict == clean_other_dict

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
