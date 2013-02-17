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


<%inherit file="/site.mako"/>


<div class="page-header">
% if user and user.slug == slug:
  <h1>My charts</h1>
% else:
  <h1>Charts of user "${slug}"</h1>
% endif
</div>

% if charts:
<ul class="charts">
    % for chart in charts:
  <li><a href="/charts/${chart.slug}">${chart.title}</a></li>
    % endfor
</ul>
% else:
<p>
    % if user and user.slug == slug:
  You have not created any chart. You can browse <a href="/charts/">all the charts</a> from the project,
  search for an existing chart using the top search bar, or
  <a href="/charts/create">create a new chart</a>.
    % else:
  This user has not created any chart.
    % endif
</p>
% endif