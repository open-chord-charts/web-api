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


"""The application's model objects"""


import collections

from . import conv, objects, wsgihelpers


# Level 1 model classes

class Model(objects.Initable, objects.JsonMapper, objects.Mapper, objects.ActivityStreamWrapper):
    @classmethod
    def json_dict_to_attributes(cls, value, state=None):
        return conv.noop(value, state=state or conv.default_state)

    def instance_to_json(self, state=None):
        values, errors = conv.object_to_clean_dict(self, state=state or conv.default_state)
        if errors is not None:
            return values, errors
        draft_id = values.pop('draft_id', None)
        if draft_id is not None:
            values['draftId'] = unicode(draft_id)
        id = values.pop('_id', None)
        if id is not None:
            values['id'] = unicode(id)
        values['published'] = self.published.isoformat()
        values['updated'] = self.updated.isoformat()
        return values, None


# Level 2 model classes

class Account(Model):
    collection_name = 'accounts'
    email = None
    password = None
    slug = None
    username = None

    def before_upsert(self, old_bson, bson):
        super(Account, self).before_upsert(old_bson, bson)
        assert self.email is not None
        assert self.password is not None
        assert self.slug is not None
        assert self.username is not None

    def compute_attributes(self):
        self.slug = conv.slugify(self.username)


class Chart(Model):
    collection_name = 'charts'
    composers = None
    keywords = None
    owner_account_id = None
    slug = None
    title = None

    @property
    def account(self):
        assert self.owner_account_id is not None
        return Account.find_one({'_id': self.owner_account_id})

    def before_upsert(self, old_bson, bson):
        super(Account, self).before_upsert(old_bson, bson)
        assert self.owner_account_id is not None

    def compute_attributes(self):
        self.keywords = self.compute_keywords()
        self.slug = conv.slugify(self.title)

    def compute_keywords(self):
        keywords = []
        keywords.extend(conv.slugify(self.title).split('-'))
        if self.composers is not None:
            keywords.extend(conv.slugify(' '.join(self.composers)).split('-'))
        return keywords

    def instance_to_json(self, state=None):
        values, errors = super(Chart, self).instance_to_json(state=state or conv.default_state)
        if errors is not None:
            return values, errors
        owner_account_id = values.pop('owner_account_id')
        values['ownerAccountId'] = unicode(owner_account_id)
        return values, None

    @classmethod
    def make_id_or_slug_to_instance(cls):
        def id_or_slug_to_instance(value, state=None):
            if value is None:
                return value, None
            if state is None:
                state = conv.default_state
            id, error = conv.str_to_object_id(value, state=state)
            if error is None:
                self = cls.find_one(id, as_class=collections.OrderedDict)
            else:
                self = cls.find_one(dict(slug=value), as_class=collections.OrderedDict)
            if self is None:
                return value, state._(u'No chart with ID or slug: {}').format(value)
            return self, None
        return id_or_slug_to_instance


# Helper functions around models

def check_owner(ctx, user, chart):
    if user._id != chart.owner_account_id:
        raise wsgihelpers.forbidden(ctx, message=ctx._(u'The authentified user is not the owner of the chart'))


def get_user(ctx, check=False):
    from . import auth
    user = ctx.user
    req = ctx.req
    if user is UnboundLocalError:
        username = ctx.session.get('username')
        if username is None:
            result = auth.authenticate(req.environ)
            if isinstance(result, basestring):
                username = req.remote_user = result
                ctx.session['username'] = username
                ctx.session.save()
            elif check:
                raise result
        ctx.user = user = None if username is None else Account.find_one({'username': username})
    return user


# Configuration functions

def init(db):
    objects.Wrapper.db = db


def setup():
    """Setup MongoDB database."""
    Account.ensure_index('email', unique=True)
    Account.ensure_index('slug', unique=True)
    Account.ensure_index('username', unique=True)
    Chart.ensure_index('keywords')
    Chart.ensure_index('owner_account_id')
    Chart.ensure_index('slug', unique=True)
    Chart.ensure_index('title', unique=True)
