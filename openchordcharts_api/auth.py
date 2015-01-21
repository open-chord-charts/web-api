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


"""Authentication functions"""


import hashlib

import webob

from . import conf, contexts, model, wsgihelpers


def authenticate(environ):
    def respond_authenticate():
        ctx = contexts.Ctx(req)
        headers = (
            ('WWW-Authenticate', u'Basic realm="{}"'.format(conf['auth.realm']).encode('utf-8')),
            )
        return wsgihelpers.unauthorized(ctx, headers=headers)

    req = webob.Request(environ)
    authorization = req.authorization
    if authorization is None:
        return respond_authenticate()
    authtype, auth = authorization
    if authtype != 'Basic':
        return respond_authenticate()
    auth = auth.decode('base64')
    username, password = auth.split(':', 1)
    if check_auth(environ, username, password):
        return username
    return respond_authenticate()


def check_auth(environ, username, password):
    password_hexdigest = hashlib.sha1(password).hexdigest()
    account = model.Account.find_one({'username': username}) \
        if conf['auth.bypass_with_username'] is not None and conf['auth.bypass_with_username'] == username \
        else model.Account.find_one({'username': username, 'password': password_hexdigest})
    environ['auth.user_account'] = account
    return account is not None
