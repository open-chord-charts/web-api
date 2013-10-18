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


"""Chart model class."""


import datetime

from biryani1.baseconv import check
from biryani1.objectconv import object_to_clean_dict
from biryani1.strings import slugify
from suq.monpyjama import Mapper

from .. import database
from .account import Account


class Chart(Mapper, database.Wrapper):
    account_id = None
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

    @property
    def account(self):
        assert self.account_id is not None
        return Account.find_one({'_id': self.account_id})

    def compute_keywords(self):
        keywords = []
        keywords.extend(slugify(self.title).split('-'))
        if self.composers is not None:
            keywords.extend(slugify(' '.join(self.composers)).split('-'))
        return keywords

    def save(self, *args, **kwargs):
        if self.created_at is None:
            self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()
        assert self.account_id is not None
        return super(Chart, self).save(*args, **kwargs)

    def to_bson(self):
        if self.slug is None:
            self.slug = slugify(self.title)
        self.keywords = self.compute_keywords()
        return check(object_to_clean_dict(self))
