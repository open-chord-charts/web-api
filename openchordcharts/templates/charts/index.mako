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


<%!
from webhelpers.html.tools import highlight
%>


<%inherit file="/site.mako"/>


<%block name="container_content">
<div class="page-header">
  <h1>
% if data['q'] is None:
    Charts
% else:
    Results for "${data['q']}"
% endif
</h1>
</div>

% if charts_cursor.count():
<ul class="charts">
    % for chart in charts_cursor:
  <li>
    <a href="/charts/${chart.slug}">
      ${highlight(chart.title, data['q'].strip().split()) if data['q'] else chart.title}
    </a>
  </li>

  % endfor
</ul>
% else:
<p>No charts found.</p>
% endif

<%
user = req.ctx.find_user()
%>
% if data['q'] is None and user is not None:
<div class="form-actions">
  <a class="btn create" href="/charts/create">Create</a>
</div>
% endif
</%block>


<%block name="domready_content">
initChartsIndex({$el: $('ul.charts')});
</%block>


<%block name="page_scripts">
<script src="/charts/index.js"></script>
</%block>
