# -*- coding: utf-8 -*-


"""Context loaded and saved in WSGI requests"""


from webob.dec import wsgify


def make_add_context_to_request(app, app_ctx):
    """Return a WSGI middleware that adds context to requests."""
    @wsgify
    def add_context_to_request(req):
        req.ctx = app_ctx
        req.ctx.req = req
        return req.get_response(app)
    return add_context_to_request


class Context(object):
    _ = lambda self, message: message
    db = None
    req = None
    session = None

    @property
    def session(self):
        return self.req.environ.get('beaker.session') if self.req is not None else None

    @property
    def user(self):
        if 'user_id' not in self.session:
            return None
        return self.db.accounts.find_one({
#            'provider_url': self.session['provider_url'],
            'user_id': self.session['user_id'],
            })
