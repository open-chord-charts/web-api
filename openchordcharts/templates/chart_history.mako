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
from babel.dates import format_datetime
%>


<%inherit file="site.mako"/>


<%block name="article">
<div class="page-header">
  <h1>
    <span class="title">${chart.title}</span>
    <small>History</small>
  </h1>
</div>

<ul>
  <li><a href="${request.route_path('chart', slug=chart.slug)}">Current version</a></li>
% for history_chart in history_charts_cursor:
  <li><a href="${request.route_path('chart', slug=chart.slug, _query=dict(revision=history_chart._id))}">\
${history_chart.title} (${format_datetime(history_chart.modified_at)})</a></li>
% endfor
</ul>

% if history_charts_cursor.count() == 0:
<p>This chart has no previous version.</p>
% endif
</%block>
