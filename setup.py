#!/usr/bin/env python
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


"""Open Chord Charts API"""


from setuptools import setup, find_packages


doc_lines = __doc__.split('\n')


setup(
    author=u'Christophe Benz',
    author_email=u'contact@openchordcharts.org',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        ],
    data_files=[
        ('share/locale/fr/LC_MESSAGES', ['openchordcharts_api/i18n/fr/LC_MESSAGES/openchordcharts-api.mo']),
        ],
    description=doc_lines[0],
    entry_points={
        'paste.app_factory': 'main = openchordcharts_api.application:make_app',
        },
    include_package_data=True,
    install_requires=[
        'Babel',
        'Beaker',
        'Biryani >= 0.10.1',
        'Paste',
        'pymongo >= 2.2',  # Comment if installed from Debian because not exposed in pyshared.
        'WebOb',
        ],
    keywords='web api chord chart music contributive',
    license=u'http://www.fsf.org/licensing/licenses/agpl-3.0.html',
    long_description='\n'.join(doc_lines[2:]),
    name=u'OpenChordCharts-API',
    packages=find_packages(),
    url=u'https://github.com/openchordcharts',
    version='0.2dev',
    zip_safe=False,
    )
