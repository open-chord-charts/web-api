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


"""Accounts controller functions."""


import hashlib

from webob.dec import wsgify

from .. import contexts, conv, model, wsgihelpers


# WSGI responses

account_already_exists = lambda ctx, username: \
    wsgihelpers.bad_request(ctx, message=ctx._(u'Account with username "{}" already exists'.format(username)))


# Controllers

@wsgify
def login(req):
    ctx = contexts.Ctx(req)
    model.get_user(ctx, check=True)
    return wsgihelpers.respond_json(ctx, {'login': 'ok'})


@wsgify
def logout(req):
    ctx = contexts.Ctx(req)
    ctx.session.delete()
    return wsgihelpers.respond_json(ctx, {'logout': 'ok'})


@wsgify
def register(req):
    ctx = contexts.Ctx(req)
    data, errors = conv.struct(
        {
            'email': conv.pipe(
                conv.str_to_email,
                conv.not_none,
                ),
            'password': conv.pipe(
                conv.empty_to_none,
                conv.not_none,
                ),
            'username': conv.pipe(
                conv.empty_to_none,
                conv.not_none,
                ),
            },
        default=None,  # Fail if unexpected item.
        )(req.params, state=ctx)
    if errors is not None:
        return wsgihelpers.bad_request(ctx, errors=errors, message=ctx._(u'Invalid parameters'))
    existing_account = model.Account.find_one({'username': data['username']})
    if existing_account is not None:
        return account_already_exists(ctx, data['username'])
    password_hexdigest = hashlib.sha1(data['password']).hexdigest()
    account = model.Account(email=data['email'], username=data['username'], password=password_hexdigest)
    account.compute_attributes()
    account.save(safe=True)
    return wsgihelpers.respond_json(ctx, {'register': 'ok'})
