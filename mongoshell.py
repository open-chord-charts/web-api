#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os

import bson
from paste.deploy import loadapp
import pymongo  # noqa


from openchordcharts.model.account import Account  # noqa
from openchordcharts.model.chart import Chart  # noqa


base_dir = os.path.abspath(os.path.dirname(__file__))
conf_file_name = 'production.ini' if os.path.exists('production.ini') else 'development.ini'
conf_file_path = os.path.join(base_dir, conf_file_name)
app = loadapp(u'config:{0}#main'.format(conf_file_path))
db = app.ctx.db
ObjectId = bson.ObjectId
