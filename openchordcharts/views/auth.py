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


import urlparse

from pyramid.exceptions import Forbidden
from pyramid.httpexceptions import HTTPBadRequest, HTTPFound
from pyramid.security import forget, remember
import wannanou

from openchordcharts.model.openidconnect import Authentication, Provider
from openchordcharts.model.user import User


def fake_login(request):
    settings = request.registry.settings
    fake_login_value = settings.get('authentication.fake_login')
    if not fake_login_value:
        raise Forbidden()
    headers = remember(request, fake_login_value)
    user = User.find_one(dict(email=fake_login_value))
    if user is None:
        user = User()
        user.email = fake_login_value
        user.save(safe=True)
    state = request.GET.get('state')
    return HTTPFound(headers=headers, location=state)


def login(request):
    callback_path = request.GET.get('callback_path')
    if callback_path and urlparse.urlsplit(callback_path)[1]:
        raise HTTPBadRequest(explanation=u'Error for "state" parameter: Value must not be an absolute URL.')
    if callback_path and callback_path.startswith('/login-callback'):
        callback_path = None

    provider, error = Provider.retrieve_updated(request)
    if error is not None:
        raise HTTPBadRequest(explanation=u'Error when looking for provider and registering as client: {}'.format(
            error))

    authentication, error = provider.new_authorize_authentication(
        prompt='select_account',
        redirect_uri=request.route_url('login_callback'),
        response_type=u'code',
        scope=u'openid email',
        use_request_object=True,
        userinfo_request=dict(
            claims=dict(
                email=dict(essential=True),
                email_verified=dict(essential=True),
                ),
            ),
        )
    if error is not None:
        raise HTTPBadRequest(explanation=u'Error when creating OpenID Connect authentication: {}'.format(error))

    authorize_url, error = authentication.generate_authorization_url()
    if error is not None:
        raise HTTPBadRequest(explanation=u'Error when generating URL of OpenID Connect authorization: {}'.format(error))

    request.session['callback_path'] = callback_path
#    request.session.save()

    return HTTPFound(location=authorize_url)


def login_callback(request):
    inputs = wannanou.extract_authorization_callback_inputs_from_params(request.GET)
    data, errors = wannanou.make_authorization_callback_inputs_to_data('code')(inputs, state=None)
    if errors is not None or data.get('error') is not None:
        raise HTTPBadRequest(
#            data=data,  # data contains a "code" item that is also a bad_request parameter => We can't use **data.
#            errors=errors,
            explanation=u'An error occurred during remote authentication',
#            inputs=inputs,
#            template_path='/login-error.mako',
            )

    authentication, error = Authentication.pop_by_authorization_callback_data(data, state=None)
    if error is not None:
        if request.session is None or request.authenticated_user is None:
            # Token is not valid and no session => Error.
            raise HTTPBadRequest(
                explanation=u'The user has already been validated or the confirmation delay has expired.',
                title=u'Remote Authentication Failed',
                )
        # Token is not valid, but a session already exists => Warn user.
        raise HTTPBadRequest(
            explanation=u'Authentication has failed, but you are already signed-in.',
            title=u'Remote Authentication Failed, but user is already authenticated',
            )

    token_data, error = authentication.request_token_by_authorization_code(state=None)
    if error is not None:
        raise HTTPBadRequest(
#            dump=error,
            explanation=u'An error occurred during remote authentication.',
            )

    userinfo, error = authentication.request_userinfo(state=None)
    if error is not None:
        raise HTTPBadRequest(
#            dump=error,
            explanation=u'An error occurred when retrieving user informations.',
            )

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

    callback_path = request.session.pop('callback_path', None)
    request.session['openid_expiration'] = authentication.expiration
#    request.session.save()

    return HTTPFound(headers=headers, location=callback_path)


def logout(request):
    state = request.GET.get('state')
    if state is None:
        state = request.route_path('index')
    headers = forget(request)
    return HTTPFound(headers=headers, location=state)
