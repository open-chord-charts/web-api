<%!
import urllib
%>\
<%def name="css()" filter="trim">
<link href="/static/lib/bootstrap-2.0.1/css/bootstrap.min.css" rel="stylesheet">
<style>
  body {
    padding-top: 60px; /* 60px to make the container go all the way to the bottom of the topbar */
  }
</style>
<link href="/static/lib/bootstrap-2.0.1/css/bootstrap-responsive.min.css" rel="stylesheet">
<link href="/static/css/style.css" rel="stylesheet">
</%def>\
<%def name="scripts()" filter="trim">
<script data-main="/static/js/main" src="/static/lib/requirejs-1.0.7/require.min.js"></script>
</%def>\
<%def name="title()" filter="trim">OpenChordCharts.org</%def>\
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="description" content="Open Chord Charts project">
    <meta name="author" content="Christophe Benz">
    <meta name="viewport" content="width=device-width; initial-scale=1.0; minimum-scale=1; maximum-scale=1.0; user-scalable=0;">
    <title><%self:title/></title>
    <%self:css/>
   </head>
  <body>

    <div class="navbar navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container">
          <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </a>
          <a class="brand" href="${request.route_path('index')}">Open Chord Charts</a>
          <div class="nav-collapse">
            <ul class="nav">
              <li${u' class="active"' if request.current_route_path() == request.route_path('charts') else '' | n}>
                <a href="${request.route_path('charts')}">Charts</a>
              </li>
            </ul>
            <form action="${request.route_path('charts')}" class="navbar-search pull-left">
              <input class="search-query" name="q" placeholder="Search" type="text" value="${request.GET.get('q', '')}">
            </form>
            <ul class="nav">
              <li${u' class="active"' if request.current_route_path() == request.route_path('about') else '' | n}>
                <a href="${request.route_path('about')}">About</a>
              </li>
            </ul>
            <ul class="nav pull-right">
% if request.user:
              <li${u' class="active"' if request.current_route_path() == \
                request.route_path('user', slug=request.user.slug) else '' | n}>
                <a href="${request.route_path('user', slug=request.user.slug)}">
                  <i class="icon-user icon-white"></i> ${request.user.slug}
                </a>
              </li>
% endif
              <li>
% if request.user:
                <a href="${request.route_path('logout', _query=dict(state=request.current_route_path()))}">Logout</a>
% else:
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
                <a href="${login_url}">Login</a>
% endif
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <div class="container">
      <%self:body/>
      <footer>
        <hr>
        <%block name="footer"/>
        <p><a href="${request.route_path('about')}">Copyright ©</a> The Open Chord Charts contributors, 2012</p>
      </footer>
    </div>

    <%self:scripts/>
  </body>
</html>
