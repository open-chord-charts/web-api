#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Open chord charts project."""


from setuptools import setup, find_packages


doc_lines = __doc__.split('\n')


setup(
    author=u'Christophe Benz',
    author_email=u'christophe.benz@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        ],
    description=doc_lines[0],
    entry_points="""
        [paste.app_factory]
        main = openchordcharts.application:make_app
        """,
    include_package_data=True,
    install_requires=[
        'Babel >= 0.9.6',
        'Biryani1 >= 0.9dev',
        'pymongo',
        'suq-monpyjama >= 0.8',
        'WebError >= 0.10',
        'WebOb >= 1.1',
        ],
    keywords='web chord charts music free collaborative',
    license=u'http://www.fsf.org/licensing/licenses/agpl-3.0.html',
    long_description='\n'.join(doc_lines[2:]),
    name=u'openchordcharts',
    packages=find_packages(),
    paster_plugins=['PasteScript'],
    setup_requires=['PasteScript >= 1.6.3'],
    url=u'http://www.openchordcharts.org/',
    version='0.1',
    zip_safe=False,
    )
