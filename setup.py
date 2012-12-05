#!/usr/bin/env python
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


import os

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()

setup(
    author=u'Christophe Benz',
    author_email=u'christophe.benz@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        "Programming Language :: Python",
        ],
    description=u'open-chord-charts',
    entry_points="""
        [paste.app_factory]
        main = openchordcharts.application:make_app
        """,
    include_package_data=True,
    install_requires=[
        'Babel >= 0.9.6',
        'Biryani >= 0.9dev',
        'pymongo >= 2.4',
        'requests >= 0.14.2',
        'suq-monpyjama >= 0.8',
        'WebError >= 0.10',
        'WebOb >= 1.1',
        ],
    keywords=u'web chord charts music',
    license=u'http://www.fsf.org/licensing/licenses/agpl-3.0.html',
    long_description=README,
    name=u'open-chord-charts',
    packages=find_packages(),
    paster_plugins=['PasteScript'],
    setup_requires=["PasteScript >= 1.6.3"],
    url=u'http://www.openchordcharts.org/',
    version='0.1',
    zip_safe=False,
    )
