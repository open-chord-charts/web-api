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


<%inherit file="site.mako"/>

<div class="page-header">
% if request.GET.get('q'):
  <h1>Search results</h1>
% else:
  <h1>All charts</h1>
% endif
</div>

% if charts.count():
<ul>
  % for chart in charts:
  <li><a href="${request.route_path('chart', slug=chart.slug)}">${chart.title}</a></li>
  % endfor
</ul>
% else:
<p>No charts found.</p>
% endif
