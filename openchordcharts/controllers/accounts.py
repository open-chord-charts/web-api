# -*- coding: utf-8 -*-


import json
import urlparse

from biryani1.baseconv import function, input_to_url_path_and_query, pipe, struct
import requests
from webob.dec import wsgify

from .. import wsgi_helpers


@wsgify
def login(req):
    """Authorization request"""
    ctx = req.ctx

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
        )(inputs, state=ctx)
    if errors is not None:
        return wsgi_helpers.bad_request(ctx, explanation=ctx._(u'Login Error: {0}').format(errors))

    request_object = {
        'api_key': ctx.conf['openid.api_key'],
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
            ctx,
            dump=response_text,
            explanation=ctx._(u'Error while generating authorize URL'),
            )
    return wsgi_helpers.redirect(ctx, location=response_json['data']['authorize_url'])


@wsgify
def login_callback(req):
    """Authorization response"""
    ctx = req.ctx

    assert req.method == 'GET'

    response_text = requests.post(
        urlparse.urljoin(req.ctx.conf['openid.api_url'], '/api/v1/user'),
        data=ctx.req.query_string,
        ).text
    response_json = json.loads(response_text)
    if 'error' in response_json:
        return wsgi_helpers.internal_error(ctx,
            dump=response_text,
            explanation=ctx._(u'Error while retrieving user infos'),
            )
    authentication = response_json['data']
    stash = authentication['stash']
    userinfo = authentication['userinfo']

    user = ctx.db.accounts.find_one({
        'provider_url': authentication['provider_url'],
        'user_id': authentication['user_id'],
        })
    if user is None:
        user = {
            'provider_url': authentication['provider_url'],
            'user_id': authentication['user_id'],
            }
    user_changed = False
    for name, userinfo_name in (
            ('email', 'email'),
            ('username', 'preferred_username'),
            ):
        value = userinfo.get(userinfo_name)
        if value != user.get(name):
            user[name] = value
            user_changed = True
    if user_changed:
        ctx.db.accounts.save(user, safe=True)
    ctx.user = user

    callback = stash.get('callback')
    response = wsgi_helpers.redirect(ctx, location=callback or '/')
    ctx.session['provider_url'] = user['provider_url']
    ctx.session['user_id'] = user['user_id']
    ctx.session.save()
    return response


@wsgify
def logout(req):
    ctx = req.ctx

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
        )(inputs, state=ctx)
    if errors is not None:
        return wsgi_helpers.bad_request(ctx, explanation=ctx._(u'Logout Error: {0}').format(errors))

    response = wsgi_helpers.redirect(ctx, location=data['callback'] or '/')
    session = ctx.session
    if session is not None:
        session.delete()
    return response
