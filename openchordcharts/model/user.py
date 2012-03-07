# -*- coding: utf-8 -*-

import datetime

from biryani.strings import slugify
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
        if self.slug is None:
            self.slug = slugify(self.email)
        return super(User, self).save(*args, **kwargs)
