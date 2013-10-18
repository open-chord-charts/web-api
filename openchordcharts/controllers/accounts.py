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


"""Accounts controller functions."""


from biryani1.baseconv import function, input_to_url_path_and_query, pipe, struct
from webob.dec import wsgify

from ..model.account import Account
from .. import conv, wsgi_helpers


@wsgify
def login_dummy(req):
    assert req.method == 'GET'
    params = req.GET
    account = Account.find_one({'username': req.ctx.conf['dummy_login.username']})
    if account is None:
        account = Account()
        account.username = req.ctx.conf['dummy_login.username']
        account.save(safe=True)
    req.ctx.session['username'] = req.ctx.conf['dummy_login.username']
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
