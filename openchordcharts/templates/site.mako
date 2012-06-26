<!DOCTYPE html>
<html>


## Open Chord Charts -- Database of free chord charts
## By: Christophe Benz <christophe.benz@gmail.com>
##
## Copyright (C) 2012 Christophe Benz
## https://gitorious.org/open-chord-charts/
##
## This file is part of Open Chord Charts.
##
## Open Chord Charts is free software; you can redistribute it and/or modify
## it under the terms of the GNU Affero General Public License as
## published by the Free Software Foundation, either version 3 of the
## License, or (at your option) any later version.
##
## Open Chord Charts is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Affero General Public License for more details.
##
## You should have received a copy of the GNU Affero General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.


<%!
from openchordcharts.helpers import get_login_url
%>


  <head>
    <meta charset="utf-8">
    <meta name="description" content="Open Chord Charts project">
    <meta name="author" content="Christophe Benz">
    <meta name="viewport" content="width=device-width; initial-scale=1.0; minimum-scale=1; maximum-scale=1.0; user-scalable=0;">
    <title><%block name="title">OpenChordCharts</%block></title>
    <%block name="css">
    <link href="${request.registry.settings['css.bootstrap']}" rel="stylesheet">
    <style>
      body {
        padding-top: 60px; /* 60px to make the container go all the way to the bottom of the topbar */
      }
    </style>
    <link href="${request.registry.settings['css.bootstrap_responsive']}" rel="stylesheet">
    <link href="/static/css/style.css" rel="stylesheet">
    </%block>
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
% if request.user:
            <div class="btn-group pull-right">
              <a class="btn dropdown-toggle" data-toggle="dropdown" href="#">
                <i class="icon-user"></i> ${request.user.email}
                <span class="caret"></span>
              </a>
              <ul class="dropdown-menu">
                <li><a href="${request.route_path('user', slug=request.user.slug)}">Profile</a></li>
                <li class="divider"></li>
                <li><a href="${request.route_path('logout', _query=dict(state=request.current_route_path()))}" \
rel="nofollow">Logout</a></li>
              </ul>
            </div>
% else:
<%
login_url = get_login_url(request)
%>
            <ul class="nav pull-right">
              <li>
                <a href="${login_url}" rel="nofollow">Login</a>
              </li>
            </ul>
% endif
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

    <%block name="script">
    <script src="${request.registry.settings['javascript.jquery']}"></script>
    <script src="${request.registry.settings['javascript.bootstrap']}"></script>
    </%block>
  </body>
</html>
