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
from pyramid.security import has_permission
%>


<%inherit file="site.mako"/>


<%def name="page_title()">
${u'Search results' if request.GET.get('q') else u'Charts'}
</%def>


<%block name="title">
<%parent:title/>: <%self:page_title/>
</%block>


<div class="page-header">
  <h1><%self:page_title/>${u' (including deleted)' if data['include_deleted'] else ''}</h1>
</div>

% if charts.count():
<ul class="unstyled">
  % for chart in charts:
  <li><a href="${request.route_path('chart', slug=chart.slug)}">${chart.title}\
${u' (deleted)' if chart.is_deleted else ''}</a></li>
  % endfor
</ul>
% else:
<p>No charts found.</p>
% endif

% if has_permission('edit', request.root, request):
<p><a class="btn btn-primary" href="${request.route_path('chart.create')}">Add a new chart</a></p>
% else:
<p>
  <a class="btn btn-primary disabled" href="#">Add a new chart</a>
  <small>Please login to add a new chart.</small>
</p>
% endif

% if nb_deleted_charts and not data['include_deleted']:
<p>
  There are deleted charts.
  <a href="${request.route_path('charts', _query=dict(include_deleted=1))}">Click here</a>
  to display them.
</p>
% endif
