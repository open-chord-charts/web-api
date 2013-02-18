# -*- coding: utf-8 -*-


from webob.dec import wsgify

from .. import wsgi_helpers


@wsgify
def login(req):
    provider_url = 'dummy'
    user = req.ctx.db.accounts.find_one({
        'provider_url': provider_url,
        'user_id': req.ctx.conf['dummy_login.user_id'],
        })
    if user is None:
        user = {
            'provider_url': provider_url,
            'user_id': req.ctx.conf['dummy_login.user_id'],
            }
        req.ctx.db.accounts.save(user, safe=True)
    req.ctx.session['provider_url'] = provider_url
    req.ctx.session['user_id'] = req.ctx.conf['dummy_login.user_id']
    req.ctx.session.save()
    return wsgi_helpers.redirect(req.ctx, location=req.GET.get('callback') or '/')
