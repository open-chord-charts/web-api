# -*- coding: utf-8 -*-


import json
import urlparse

from biryani1.baseconv import function, input_to_url_path_and_query, pipe, struct
import requests
from webob.dec import wsgify

from ..model.account import Account
from .. import conv, wsgi_helpers


@wsgify
def login(req):
    """Authorization request"""
    assert req.method == 'GET'
    params = req.GET
    inputs = {'callback': params.get('callback')}
    data, errors = struct(
        {
            'callback': pipe(
                input_to_url_path_and_query,
                function(lambda callback: None if callback.startswith(('/login', '/logout')) else callback),
                ),
            },
        )(inputs, state=conv.default_state)
    if errors is not None:
        return wsgi_helpers.bad_request(req.ctx, explanation=req.ctx._(u'Login Error: {0}').format(errors))

    request_object = {
        'api_key': req.ctx.conf['openid.api_key'],
        'redirect_uri': req.host_url + '/login-callback',
        'prompt': 'select_account',
        'response_type': u'code',
        'scope': u'openid email',
        'stash': data,
        'userinfo': {
            'claims': {
                'email': None,
                'email_verified': None,
                'preferred_username': None,
                },
            },
        }
    response_text = requests.post(
        urlparse.urljoin(req.ctx.conf['openid.api_url'], '/api/v1/authorize-url'),
        data=json.dumps(request_object, encoding='utf-8', ensure_ascii=False, indent=2, sort_keys=True),
        headers={'Content-Type': 'application/json; charset=utf-8'},
        ).text
    response_json = json.loads(response_text)
    if 'error' in response_json:
        return wsgi_helpers.internal_error(
            req.ctx,
            dump=response_text,
            explanation=req.ctx._(u'Error while generating authorize URL'),
            )
    return wsgi_helpers.redirect(req.ctx, location=response_json['data']['authorize_url'])


@wsgify
def login_callback(req):
    """Authorization response"""
    assert req.method == 'GET'
    response_text = requests.post(
        urlparse.urljoin(req.ctx.conf['openid.api_url'], '/api/v1/user'),
        data=req.query_string,
        ).text
    response_json = json.loads(response_text)
    if 'error' in response_json:
        return wsgi_helpers.internal_error(req.ctx,
            dump=response_text,
            explanation=req.ctx._(u'Error while retrieving user infos'),
            )
    authentication = response_json['data']
    stash = authentication['stash']
    userinfo = authentication['userinfo']

    user = Account.find_one({
        'provider_url': authentication['provider_url'],
        'user_id': authentication['user_id'],
        })
    if user is None:
        user = Account()
        user.provider_url = authentication['provider_url']
        user.user_id = authentication['user_id']
    user_changed = False
    for name, userinfo_name in (
            ('email', 'email'),
            ('username', 'preferred_username'),
            ):
        value = userinfo.get(userinfo_name)
        if value != getattr(user, name):
            setattr(user, name, value)
            user_changed = True
    if user_changed:
        user.save(safe=True)

    callback = stash.get('callback')
    response = wsgi_helpers.redirect(req.ctx, location=callback or '/')
    req.ctx.session['provider_url'] = authentication['provider_url']
    req.ctx.session['user_id'] = authentication['user_id']
    req.ctx.session.save()
    return response


@wsgify
def login_dummy(req):
    assert req.method == 'GET'
    params = req.GET
    user = Account.find_one({
        'user_id': req.ctx.conf['dummy_login.user_id'],
        })
    if user is None:
        user = Account()
        user.dummy = True
        user.user_id = req.ctx.conf['dummy_login.user_id']
        user.save(safe=True)
    req.ctx.session['user_id'] = req.ctx.conf['dummy_login.user_id']
    req.ctx.session.save()
    return wsgi_helpers.redirect(req.ctx, location=params.get('callback') or '/')


@wsgify
def logout(req):
    assert req.method == 'GET'
    params = req.GET
    inputs = {'callback': params.get('callback')}
    data, errors = struct(
        {
            'callback': pipe(
                input_to_url_path_and_query,
                function(lambda callback: None if callback.startswith(('/login', '/logout')) else callback),
                ),
            },
        )(inputs, state=conv.default_state)
    if errors is not None:
        return wsgi_helpers.bad_request(req.ctx, explanation=req.ctx._(u'Logout Error: {0}').format(errors))
    response = wsgi_helpers.redirect(req.ctx, location=data['callback'] or '/')
    req.ctx.session.delete()
    return response
