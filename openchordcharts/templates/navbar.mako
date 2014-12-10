## -*- coding: utf-8 -*-

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


<nav class="navbar navbar-fixed-top">
  <div class="navbar-inner">
    <div class="container">
      <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </a>
      <a class="brand" href="/">Open Chord Charts (beta)</a>
      <div class="nav-collapse">
        <ul class="nav">
          <li${u' class="active"' if req.path.startswith('/charts') else '' | n}>
            <a class="charts" href="/charts/">Charts</a>
          </li>
        </ul>
        <form action="/charts" class="navbar-search" method="get">
          <input class="search-query" name="q" placeholder="Example: All of me" type="search" \
value="${req.GET.get('q') or ''}">
        </form>
% if req.ctx.user:
        <div class="btn-group pull-right">
          <a class="btn dropdown-toggle" data-toggle="dropdown" href="#">
           <i class="icon-user"></i> ${req.ctx.user.username}
            <span class="caret"></span>
          </a>
          <ul class="dropdown-menu">
            <li><a class="my-charts" href="/users/${req.ctx.user.slug}">My charts</a></li>
            <li class="divider"></li>
            <li><a href="/logout?callback=${req.path}" rel="nofollow">Logout</a></li>
          </ul>
        </div>
% else:
        <ul class="nav pull-right">
          <li>
            <a class="login" href="/login?callback=${req.path}" rel="nofollow">Login</a>
          </li>
        </ul>
% endif
      </div>
    </div>
  </div>
</nav>
