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

from biryani.strings import slugify
from biryani.baseconv import check
from biryani.objectconv import object_to_clean_dict
from suq.monpyjama import Mapper, Wrapper


class User(Mapper, Wrapper):
    collection_name = 'users'

    created_at = None
    email = None
    modified_at = None
    slug = None

    def save(self, *args, **kwargs):
        if self.created_at is None:
            self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()
        return super(User, self).save(*args, **kwargs)

    def to_bson(self):
        if self.slug is None:
            self.slug = slugify(self.email)
        return check(object_to_clean_dict(self))
