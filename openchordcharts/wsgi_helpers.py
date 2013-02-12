# -*- coding: utf-8 -*-


import collections
import json

from markupsafe import Markup
from webhelpers.html import tags
import webob.dec
import webob.exc

from . import templates


N_ = lambda message: message


errors_explanation = {
    400: N_("Request is faulty"),
    401: N_("Access is restricted to authorized persons."),
    403: N_("Access is forbidden."),
    404: N_("The requested page was not found."),
    }
errors_message = {
    401: N_("You must login to access this page."),
    }
errors_title = {
    400: N_("Unable to Access"),
    401: N_("Access Denied"),
    403: N_("Access Denied"),
    404: N_("Unable to Access"),
    }


def bad_request(ctx, **kw):
    return error(ctx, 400, **kw)


def discard_empty_items(data):
    if isinstance(data, collections.Mapping):
        # Use type(data) to keep OrderedDicts.
        data = type(data)(
            (name, discard_empty_items(value))
            for name, value in data.iteritems()
            if value is not None
            )
    return data


def error(ctx, code, **kw):
    response = webob.exc.status_map[code](headers=kw.pop('headers', None))
    if code != 204:  # No content
        body = kw.pop('body', None)
        if body is None:
            template_path = kw.pop('template_path', '/http-error.mako')
            explanation = kw.pop('explanation', None)
            if explanation is None:
                explanation = errors_explanation.get(code)
                explanation = ctx._(explanation) if explanation is not None else response.explanation
            message = kw.pop('message', None)
            if message is None:
                message = errors_message.get(code)
                if message is not None:
                    message = ctx._(message)
            comment = kw.pop('comment', None)
            if isinstance(comment, dict):
                comment = tags.ul(u'{0} : {1}'.format(key, value) for key, value in comment.iteritems())
            elif isinstance(comment, list):
                comment = tags.ul(comment)
            title = kw.pop('title', None)
            if title is None:
                title = errors_title.get(code)
                title = ctx._(title) if title is not None else response.status
            body = templates.render(
                ctx,
                template_path,
                comment=comment,
                explanation=explanation,
                message=message,
                response=response,
                title=title,
                **kw
                )
        response.body = body.encode('utf-8') if isinstance(body, unicode) else body
    return response


def forbidden(ctx, **kw):
    return error(ctx, 403, **kw)


def method_not_allowed(ctx, **kw):
    return error(ctx, 405, **kw)


def no_content(ctx, headers=None):
    return error(ctx, 204, headers=headers)


def not_found(ctx, **kw):
    return error(ctx, 404, **kw)


def redirect(ctx, code=302, location=None, **kw):
    assert location is not None
    location_str = location.encode('utf-8') if isinstance(location, unicode) else location
    response = webob.exc.status_map[code](headers=kw.pop('headers', None), location=location_str)
    body = kw.pop('body', None)
    if body is None:
        template_path = kw.pop('template_path', '/http-error.mako')
        explanation = kw.pop('explanation', None)
        if explanation is None:
            explanation = Markup(u'{0} <a href="{1}">{1}</a>.').format(ctx._(u"You'll be redirected to page"), location)
        message = kw.pop('message', None)
        if message is None:
            message = errors_message.get(code)
            if message is not None:
                message = ctx._(message)
        title = kw.pop('title', None)
        if title is None:
            title = ctx._("Redirection in progress...")
        body = templates.render(
            ctx,
            template_path,
            comment=kw.pop('comment', None),
            explanation=explanation,
            message=message,
            response=response,
            title=title,
            **kw
            )
    response.body = body.encode('utf-8') if isinstance(body, unicode) else body
    return response


def respond_json(ctx, data, code=None, headers=None, jsonp=None):
    """Return a JSON response.

    This function is optimized for JSON following
    `Google JSON Style Guide <http://google-styleguide.googlecode.com/svn/trunk/jsoncstyleguide.xml>`_, but will handle
    any JSON except for HTTP errors.
    """
    if isinstance(data, collections.Mapping):
        # Remove null properties as recommended by Google JSON Style Guide.
        data = discard_empty_items(data)
        error = data.get('error')
    else:
        error = None
    if headers is None:
        headers = []
    if jsonp:
        headers.append(('Content-Type', 'application/javascript; charset=utf-8'))
    else:
        headers.append(('Content-Type', 'application/json; charset=utf-8'))
    if error:
        code = code or error['code']
        assert isinstance(code, int)
        response = webob.exc.status_map[code](headers=headers)
        if error.get('code') is None:
            error['code'] = code
        if error.get('message') is None:
            error['message'] = response.title
    else:
        response = ctx.req.response
        if code is not None:
            response.status = code
        response.headers.update(headers)
    text = unicode(json.dumps(data, encoding='utf-8', ensure_ascii=False, indent=2, sort_keys=True))
    if jsonp:
        text = u'{0}({1})'.format(jsonp, text)
    response.text = text
    return response


def unauthorized(ctx, **kw):
    return error(ctx, 401, **kw)
