# -*- coding: utf-8 -*-


# Open Chord Charts -- Database of free chord charts
# By: Christophe Benz <contact@openchordcharts.org>
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

from biryani1.baseconv import check
from biryani1.objectconv import object_to_clean_dict
from biryani1.strings import slugify
from suq.monpyjama import Mapper, Wrapper


class Chart(Mapper, Wrapper):
    account_id = None
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

    def compute_keywords(self):
        keywords = []
        keywords.extend(self.slug.split('-'))
        if self.composers is not None:
            keywords.extend(slugify(' '.join(self.composers)).split('-'))
        return keywords

    def generate_unique_slug(self):
        title_slug = slugify(self.title)
        slug = title_slug
        slug_index = 1
        while True:
            spec = {'slug': slug}
            if Chart.find_one(spec) is None:
                return slug
            else:
                slug = u'{0}-{1}'.format(title_slug, slug_index)
                slug_index += 1

    def save(self, *args, **kwargs):
        if self.created_at is None:
            self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()
        return super(Chart, self).save(*args, **kwargs)

    def to_bson(self):
        if self.slug is None:
            self.slug = self.generate_unique_slug()
        self.keywords = self.compute_keywords()
        return check(object_to_clean_dict(self))
