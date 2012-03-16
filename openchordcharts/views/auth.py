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


import base64
import datetime
import json
import urllib
import urllib2
import urlparse

from pyramid.httpexceptions import HTTPBadRequest, HTTPFound
from pyramid.security import forget, remember
from pyramid.view import view_config

from openchordcharts.model.user import User


@view_config(route_name='login_callback')
def login_callback(request):
    params = request.GET
    settings = request.registry.settings

    if params.get('error') is not None:
        raise HTTPBadRequest(detail=params['error'])

    code = params.get('code')
    if not code:
        raise HTTPBadRequest(detail=u'Missing value')

    state = params.get('state')
    if state and urlparse.urlsplit(state)[1]:
        raise HTTPBadRequest(detail=u'state must not be an absolute URL.')
    if not state:
        state = request.route_path('index')

    # Request access token.
    try:
        resp = urllib2.urlopen(settings['oauth.token_url'], urllib.urlencode(dict(
            client_id=settings['oauth.client_id'],
            client_secret=settings['oauth.client_secret'],
            code=code,
            grant_type='authorization_code',
            redirect_uri=request.route_url('login_callback'),
            scope=settings['oauth.scope.auth'],
            )))
    except urllib2.HTTPError, resp:
        if resp.code == 400:
            raise HTTPBadRequest(detail=resp.read())
        else:
            raise
    access_token_infos = json.load(resp, encoding='utf-8')
    access_token_infos['expiration'] = datetime.datetime.now() + datetime.timedelta(
        seconds=access_token_infos.get('expires_in'))
    print u'OAuth token response params: {0}'.format(access_token_infos).encode('utf-8')

    # get/extract email from access token
    email = json.loads(
        base64.urlsafe_b64decode(str(access_token_infos['access_token']).split('.')[1]))['prn']['email']

    user = User.find_one(dict(email=email))
    if user is None:
        user = User()
        user.email = email
        user.save(safe=True)
    headers = remember(request, user.email)
    return HTTPFound(headers=headers, location=state)


@view_config(route_name='logout')
def logout(request):
    state = request.GET.get('state')
    if state is None:
        state = request.route_path('index')
    headers = forget(request)
    return HTTPFound(headers=headers, location=state)
