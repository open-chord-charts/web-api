<%!
import urllib
%>\
<%def name="css()" filter="trim">
</%def>\
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <%self:css/>
    </head>
    <body>
        <h1>Open Chord Charts</h1>
<%
settings = request.registry.settings
login_url = settings['oauth.authorize_url'] + '?' + urllib.urlencode(dict(
    (name, value)
    for name, value in dict(
        client_id=settings['oauth.client_id'],
        redirect_uri=request.route_url('login_callback'),
        response_type='code',
        scope=settings['oauth.scope.auth'],
        state=request.path_qs,
        ).iteritems()
    if value is not None
    ))
%>\
% if request.session.get('email'):
        ${request.session['email']}: <a href="${request.route_path('logout')}">Logout</a>
% else:
        <a href="${login_url}">Login</a>
% endif
        <%self:body/>
    </body>
</html>
