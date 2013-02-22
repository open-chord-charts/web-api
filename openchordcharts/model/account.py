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


class Account(Mapper, Wrapper):
    collection_name = 'accounts'
    created_at = None
    email = None
    modified_at = None
    slug = None
    user_id = None
    username = None

    def generate_unique_slug(self):
        username_slug = slugify(self.username)
        slug = username_slug
        slug_index = 1
        while True:
            if Account.find_one({'slug': slug}) is None:
                return slug
            else:
                slug = u'{0}-{1}'.format(username_slug, slug_index)
                slug_index += 1

    def save(self, *args, **kwargs):
        if self.created_at is None:
            self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()
        return super(Account, self).save(*args, **kwargs)

    def to_bson(self):
        if self.slug is None or self.slug != slugify(self.user_id):
            self.slug = self.generate_unique_slug()
        return check(object_to_clean_dict(self))
