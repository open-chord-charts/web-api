# -*- coding: utf-8 -*-

from suq.monpyjama import Mapper, Wrapper


class User(Mapper, Wrapper):
    collection_name = 'users'

    email = None
    name = None
