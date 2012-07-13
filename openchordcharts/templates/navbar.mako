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


<nav class="navbar navbar-fixed-top">
  <div class="navbar-inner">
    <div class="container">
      <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </a>
      <a class="brand" href="${request.route_path('index')}">Open Chord Charts (dev)</a>
      <div class="nav-collapse">
        <ul class="nav">
          <li${u' class="active"' if request.matched_route.name == 'charts' else '' | n}>
            <a class="charts" href="${request.route_path('charts')}">Charts</a>
          </li>
        </ul>
        <div class="navbar-search">
          <input class="search-query" placeholder="Search (ex: All of me)" type="search">
        </div>
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
        <ul class="nav pull-right">
          <li>
            <a class="login" href="${get_login_url(request)}" rel="nofollow">Login</a>
          </li>
        </ul>
% endif
      </div>
    </div>
  </div>
</nav>
