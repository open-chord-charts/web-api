## -*- coding: utf-8 -*-


## Open Chord Charts -- Database of free chord charts
## By: Christophe Benz <contact@openchordcharts.org>
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


<%inherit file="/site.mako"/>


<%block name="container_content">
<%
user = req.ctx.find_user()
%>
<div class="page-header">
% if user is not None and user.slug == req.urlvars.get('slug'):
  <h1>My charts</h1>
% else:
  <h1>Charts owned by "${req.urlvars.get('slug')}"</h1>
% endif
</div>

% if charts_cursor.count():
<ul class="charts">
    % for chart in charts_cursor:
  <li><a href="/charts/${chart.slug}">${chart.title}</a></li>
    % endfor
</ul>
% else:
<p>
    % if user is not None and user.slug == req.urlvars.get('slug'):
  You don't have created any chart yet. You can browse <a href="/charts/">all the charts</a> from the project,
  search for an existing chart using the top search bar, or
  <a href="/charts/create">create a new chart</a>.
    % else:
  This user has not created any chart.
    % endif
</p>
% endif
</%block>


<%block name="domready_content">
initMobileList({$el: $('ul.charts')});
</%block>


<%block name="page_scripts">
<script src="/mobile_list.js"></script>
</%block>
