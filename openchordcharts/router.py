# -*- coding: utf-8 -*-


"""Helpers for URLs"""


import re

from webob.dec import wsgify

from . import wsgi_helpers


def make_router(*routings):
    """Return a WSGI application that dispatches requests to controllers."""
    routes = []
    for routing in routings:
        methods, regex, app = routing[:3]
        if isinstance(methods, basestring):
            methods = (methods,)
        vars = routing[3] if len(routing) >= 4 else {}
        routes.append((methods, re.compile(regex), app, vars))

    @wsgify
    def router(req):
        """Dispatch request to controllers."""
        split_path_info = req.path_info.split('/')
        assert not split_path_info[0], split_path_info
        for methods, regex, app, vars in routes:
            if methods is None or req.method in methods:
                match = regex.match(req.path_info)
                if match is not None:
                    if getattr(req, 'urlvars', None) is None:
                        req.urlvars = {}
                    req.urlvars.update(dict(
                        (name, value.decode('utf-8') if value is not None else None)
                        for name, value in match.groupdict().iteritems()
                        ))
                    req.urlvars.update(vars)
                    req.script_name += req.path_info[:match.end()]
                    req.path_info = req.path_info[match.end():]
                    return req.get_response(app)
        return wsgi_helpers.not_found(req.ctx)
    return router
