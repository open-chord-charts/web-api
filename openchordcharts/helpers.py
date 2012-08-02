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


import hashlib
import os
import subprocess

import pyramid.threadlocal


def get_git_revision():
    git_revparse_process = subprocess.Popen(['/usr/bin/git', 'rev-parse', '--verify', 'HEAD'],
        cwd=os.path.dirname(__file__), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    git_revision = git_revparse_process.stdout.read().strip()
    return git_revision if len(git_revision.split()) == 1 else None


def get_login_url(request):
    settings = request.registry.settings
    if settings['authentication.fake_login']:
        return request.route_path('fake_login', _query=dict(callback_path=request.path_qs))
    elif settings['authentication.openid.api_key']:
        return request.route_path('openidconnect_login', _query=dict(callback_path=request.path_qs))
    else:
        return None


def get_revision_hash():
    settings = pyramid.threadlocal.get_current_registry().settings
    git_revision = get_git_revision()
    if settings['development_mode']:
        git_diff_process = subprocess.Popen(['/usr/bin/git', 'diff', 'HEAD'], cwd=os.path.dirname(__file__),
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        git_diff_hash = hashlib.sha256(git_diff_process.stdout.read().strip()).hexdigest()
        return u'{0}-{1}-{2}'.format(git_revision, git_diff_hash, hash(frozenset(settings.items())))
    else:
        return git_revision
