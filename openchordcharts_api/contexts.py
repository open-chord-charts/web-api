# -*- coding: utf-8 -*-


# Open Chord Charts -- Database of free chord charts
# By: Christophe Benz <contact@openchordcharts.org>
#
# Copyright (C) 2012, 2013, 2014 Christophe Benz
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


"""Context loaded and saved in WSGI requests"""


from biryani.states import State


class Ctx(State):
    env_keys = ('_node', '_user')
    _ = lambda self, message: message
    _node = None  # Used by route functions to store model object matching id or slug in URL.
    _user = UnboundLocalError
    req = None

    def __init__(self, req=None):
        if req is not None:
            self.req = req
            ctx_env = req.environ.get('open-chord-charts', {})
            for key in self.env_keys:
                value = ctx_env.get(key)
                if value is not None:
                    setattr(self, key, value)

    def node_del(self):
        del self._node
        if self.req is not None and self.req.environ.get('open-chord-charts') is not None \
                and '_node' in self.req.environ['open-chord-charts']:
            del self.req.environ['open-chord-charts']['_node']

    def node_get(self):
        return self._node

    def node_set(self, node):
        self._node = node
        if self.req is not None:
            self.req.environ.setdefault('open-chord-charts', {})['_node'] = node

    node = property(node_get, node_set, node_del)

    @property
    def session(self):
        return self.req.environ.get('beaker.session') if self.req is not None else None

    def user_del(self):
        del self._user
        if self.req is not None and self.req.environ.get('open-chord-charts') is not None \
                and '_user' in self.req.environ['open-chord-charts']:
            del self.req.environ['open-chord-charts']['_user']

    def user_get(self):
        return self._user

    def user_set(self, user):
        self._user = user
        if self.req is not None:
            self.req.environ.setdefault('open-chord-charts', {})['_user'] = user

    user = property(user_get, user_set, user_del)
