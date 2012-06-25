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

from openchordcharts.model.user import User


def login(request):
    settings = request.registry.settings
    headers = remember(request, settings['authentication.fake_login'])
    user = User.find_one(dict(email=settings['authentication.fake_login']))
    if user is None:
        user = User()
        user.email = settings['authentication.fake_login']
        user.save(safe=True)
    callback_path = request.GET.get('callback_path')
    return HTTPFound(headers=headers, location=callback_path or request.route_path('index'))
