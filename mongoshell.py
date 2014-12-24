#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os

import bson
from paste.deploy import loadapp
import pymongo  # noqa


from openchordcharts_api import environment
from openchordcharts_api.model import Account, Chart  # noqa


base_dir = os.path.abspath(os.path.dirname(__file__))
conf_file_name = 'production.ini' if os.path.exists('production.ini') else 'development.ini'
conf_file_path = os.path.join(base_dir, conf_file_name)
app = loadapp(u'config:{}#api'.format(conf_file_path))
db = environment.db
ObjectId = bson.ObjectId
