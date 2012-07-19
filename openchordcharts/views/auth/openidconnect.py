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


import json
import urlparse

from pyramid.httpexceptions import HTTPBadRequest, HTTPFound
from pyramid.security import remember
import requests

from openchordcharts.model.user import User


def login(request):
    settings = request.registry.settings

    callback_path = request.GET.get('callback_path')
    if callback_path and urlparse.urlsplit(callback_path)[1]:
        raise HTTPBadRequest(explanation=u'Error for "state" parameter: Value must not be an absolute URL.')
    if callback_path and callback_path.startswith('/login-callback'):
        callback_path = None

    request_object = dict(
        api_key=settings['authentication.openid.api_key'],
#        client_id=settings['authentication.openid.client_id'],
#        client_secret=settings['authentication.openid.client_secret'],
        prompt='select_account',
        redirect_uri=request.route_url('login_callback'),
        scope=u'openid email',
        stash=dict(callback_path=callback_path),
        userinfo=dict(
            claims=dict(
                email=dict(essential=True),
                email_verified=dict(essential=True),
                ),
            ),
        )
    response_text = requests.post(urlparse.urljoin(settings['authentication.openid.api_url'], '/api/v1/authorize-url'),
        data=json.dumps(request_object, encoding='utf-8', ensure_ascii=False, indent=2, sort_keys=True),
        headers={
            'Content-Type': 'application/json; charset=utf-8',
            },
        ).text
    response_json = json.loads(response_text)
    if 'error' in response_json:
        raise HTTPBadRequest(
            detail=response_text,
            explanation=u'Error while generating authorize URL',
            )
    return HTTPFound(location=response_json['data']['authorize_url'])


def login_callback(request):
    settings = request.registry.settings

    response_text = requests.post(urlparse.urljoin(settings['authentication.openid.api_url'], '/api/v1/user'),
        data=request.query_string,
        ).text
    response_json = json.loads(response_text)
    if 'error' in response_json:
        raise HTTPBadRequest(
            detail=response_text,
            explanation=u'Error while retrieving user infos',
            )
    authentication = response_json['data']
    userinfo = authentication['userinfo']

    email = userinfo.get('email')
    if email is None:
        raise HTTPBadRequest(
            explanation=u'Email missing.',
            )
    email_verified = userinfo.get('email_verified')
    if not email_verified:
        raise HTTPBadRequest(
            explanation=u'Email not confirmed.',
            )
    user = User.find_one(dict(email=email))
    if user is None:
        user = User()
        user.email = email
        user.save(safe=True)
    headers = remember(request, user.email)

    return HTTPFound(headers=headers, location=authentication['stash']['callback_path'] or request.route_path('index'))
