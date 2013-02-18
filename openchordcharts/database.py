# -*- coding: utf-8 -*-


"""Database loading functions."""


import pymongo
import suq.monpyjama


def ensure_indexes(ctx):
    ctx.db.accounts.ensure_index([('email', pymongo.ASCENDING)])
    ctx.db.accounts.ensure_index([('user_id', pymongo.ASCENDING)])
    ctx.db.charts.ensure_index([('keywords', pymongo.ASCENDING)])
    ctx.db.charts.ensure_index([('slug', pymongo.ASCENDING)])
    ctx.db.charts.ensure_index([('title', pymongo.ASCENDING)])
    ctx.db.charts.ensure_index([('user', pymongo.ASCENDING)])


def load_database(ctx):
    connection = pymongo.Connection(host=ctx.conf['database.host_name'], port=ctx.conf['database.port'])
    db = connection[ctx.conf['database.name']]
    suq.monpyjama.Wrapper.db = db
    return db
