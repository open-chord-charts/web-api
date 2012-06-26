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

from biryani.baseconv import check, function, noop, pipe, struct
from biryani.objectconv import make_dict_to_object, object_to_clean_dict
import pyramid.threadlocal
from suq.monpyjama import Mapper, Wrapper
import wannanou
import wannanou.conv


class Authentication(wannanou.abstract.Authentication, Mapper, Wrapper):
    collection_name = 'wannanou_authentications'
    to_bson = check(pipe(
        object_to_clean_dict,
        function(lambda bson: (bson.pop('_provider', None) or True) and bson),
        ))

    @classmethod
    def get_by_state(cls, authentication_state, state=None):
        return cls.find_one(dict(state=authentication_state))

    def index_by_state(self, state=None):
        self.save(safe=True)

    @classmethod
    def remove_expired(cls, state=None):
        cls.remove(dict(expiration={'$lt': datetime.datetime.utcnow()}))

    def remove_state(self, state=None):
        assert self.state is not None
        del self.state


class Client(wannanou.ramdb.Client, Mapper):
    to_bson = check(object_to_clean_dict)


class Provider(wannanou.abstract.Provider, Wrapper):
    collection_name = 'cosmetic_providers'
    to_bson = check(pipe(
        object_to_clean_dict,
        struct(
            dict(
                client=function(lambda client: client.to_bson()),
                ),
            default=noop,
            ),
        ))

    @classmethod
    def from_bson(cls, bson):
        return check(pipe(
            struct(
                dict(
                    client=function(Client.from_bson),
                    ),
                default=noop,
                ),
            make_dict_to_object(cls),
            ))(bson)

    @classmethod
    def get_by_url(cls, url, state=None):
        return cls.find_one(dict(url=url))

    def index_by_url(self, state=None):
        assert self.url is not None
        self.save(safe=True)

    @classmethod
    def remove_expired(cls, state=None):
        cls.remove(dict(expiration={'$lt': datetime.datetime.utcnow()}))

    @classmethod
    def retrieve_updated(cls, request, state=None):
        settings = pyramid.threadlocal.get_current_registry().settings
        if state is None:
            state = wannanou.conv.default_state
        self, error = cls.retrieve(settings['authentication.openid.provider_url'], state=state)
        if error is not None:
            return self, state._(u'Error while retrieving configuration of OpenID Connect server: {0}').format(error)

        client = self.client
        if client is None:
            client, error = self.configure_client(
                application_name=settings['authentication.openid.application_name'],
                client_id=settings['authentication.openid.client_id'],
                client_secret=settings['authentication.openid.client_secret'],
#                contacts=[settings['email_to']] if settings['email_to'] is not None else None,
                redirect_uris=[
                    request.route_url('login_callback'),
                    ],
                static_client_id=True,
                )
            if error is not None:
                return client, state._(u'Error while configuring OpenID Connect client: {0}').format(error)

        if client.registration is None:
            client_registration, error = self.register_client(state=state)
            if error is not None:
                return client, state._(u'Error while registering OpenID Connect client: {0}').format(error)

        return self, None
