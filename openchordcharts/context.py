# -*- coding: utf-8 -*-


"""Context loaded and saved in WSGI requests"""


from webob.dec import wsgify


def make_add_context_to_request(app, app_ctx):
    """Return a WSGI middleware that adds context to requests."""
    @wsgify
    def add_context_to_request(req):
        req_ctx = Context.from_ctx(app_ctx)
        req_ctx.req = req
        req.ctx = req_ctx
        return req.get_response(app)
    return add_context_to_request


class Context(object):
    _ = lambda self, message: message
    req = None
    session = None

    @classmethod
    def from_ctx(cls, ctx):
        new_ctx = Context()
        for key, value in ctx.__dict__.iteritems():
            new_ctx.__dict__[key] = value
        return new_ctx

    @property
    def session(self):
        return self.req.environ.get('beaker.session') if self.req is not None else None
