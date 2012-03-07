# -*- coding: utf-8 -*-

from pyramid.decorator import reify
from pyramid.request import Request
from pyramid.security import unauthenticated_userid

from openchordcharts.model.user import User


class RequestWithUserAttribute(Request):
    @reify
    def user(self):
        user_email = unauthenticated_userid(self)
        if user_email is not None:
            return User.find_one(dict(email=user_email))
