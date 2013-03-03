# -*- coding: utf-8 -*-


# Open Chord Charts -- Database of free chord charts
# By: Christophe Benz <contact@openchordcharts.org>
#
# Copyright (C) 2012-2013 Christophe Benz
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


from webob.dec import wsgify

from .model.account import Account


def make_add_context_to_request(app, app_ctx):
    """Return a WSGI middleware that adds context to requests."""
    @wsgify
    def add_context_to_request(req):
        req.ctx = app_ctx
        req.ctx.req = req
        return req.get_response(app)
    return add_context_to_request


class Context(object):
    _ = lambda self, message: message
    conf = None
    db = None
    req = None

    def find_user(self):
        if 'user_id' in self.session:
            if self.conf['dummy_login.user_id'] is not None:
                return Account.find_one({
                    'user_id': self.conf['dummy_login.user_id'],
                    })
            else:
                return Account.find_one({
                    'provider_url': self.session['provider_url'],
                    'user_id': self.session['user_id'],
                    })
        return None

    @property
    def session(self):
        return self.req.environ.get('beaker.session') if self.req is not None else None
