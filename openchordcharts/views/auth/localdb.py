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


from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember

from openchordcharts.auth import encrypt_password
from openchordcharts.model.user import User


def login(request):
    if request.method == 'POST':
        data = dict(
            email=request.params.get('email'),
            password=request.params.get('password'),
            )
        user = User.find_one(dict(email=data['email']))
        if user is None:
            errors = dict(email=u'Invalid email')
        elif user.password_sha256 != encrypt_password(data['password']):
            errors = dict(password=u'Invalid password')
        if errors is None:
            headers = remember(request, user.email)
            return HTTPFound(headers=headers, location=request.params.get('state') or request.route_path('index'))
    else:
        data = errors = None
    return dict(
        data=data or dict(),
        errors=errors or dict(),
        )
