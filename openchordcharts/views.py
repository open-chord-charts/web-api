# -*- coding: utf-8 -*-

import base64
import datetime
import json
import urllib
import urllib2
import urlparse

from pyramid.exceptions import Forbidden, NotFound
from pyramid.httpexceptions import HTTPBadRequest, HTTPFound
from pyramid.view import view_config

from . import model


@view_config(route_name='chart', renderer='/chart.mako')
def chart(request):
    slug = request.matchdict.get('slug')
    if not slug:
        return Forbidden()
    chart = model.Chart.find_one(dict(slug=slug))
    if chart is None:
        return NotFound()
    return dict(
        chart=chart,
        )


@view_config(route_name='charts', renderer='/charts.mako')
def charts(request):
    charts = model.Chart.find().limit(100)
    return dict(
        charts=charts,
        )


@view_config(route_name='index', renderer='/index.mako')
def index(request):
    return dict()


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
    access_token_infos = json.load(resp, encoding = 'utf-8')
    access_token_infos['expiration'] = datetime.datetime.now() + datetime.timedelta(
        seconds = access_token_infos.get('expires_in'))
    print u'OAuth token response params: {0}'.format(access_token_infos).encode('utf-8')

    # get/extract email from access token
    email = json.loads(
        base64.urlsafe_b64decode(str(access_token_infos['access_token']).split('.')[1]))['prn']['email']
    request.session['email'] = email

    return HTTPFound(location=state)


@view_config(route_name='logout')
def logout(request):
    request.session.pop('email', None)
    return HTTPFound(location=request.route_path('index'))
