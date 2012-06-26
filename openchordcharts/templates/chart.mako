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

<%!
from pyramid.security import has_permission

from openchordcharts.helpers import iter_chords, iter_parts, render_chord
from openchordcharts.utils import common_chromatic_keys
%>

<%def name="css()" filter="trim">
<%parent:css/>
<link href="/static/css/chart.css" rel="stylesheet">
</%def>

<div class="page-header">
  <h1>
    <span class="title">${chart.title}</span>
% if chart.composers:
    <small class="composers">${u', '.join(chart.composers)}</small>
% endif
  </h1>
</div>

% if chart.is_deleted:
<div class="alert alert-block">
  <a class="close" data-dismiss="alert">×</a>
  <h4 class="alert-heading">Warning!</h4>
  <p>This chart is marked as deleted.</p>
</div>
% endif

% if chart.genre or chart.structure:
<p class="structure-genre">
  % if chart.structure:
  <span class="structure">${len(list(chart.iter_chords()))} × ${''.join(chart.structure)}</span>
  % endif
  % if chart.genre:
  <small class="genre">${chart.genre}</small>
  % endif
</p>
% endif

% if chart.structure:
<div class="chords">
  % for part_name, part_occurence in iter_parts(chart):
  <div class="part ${'repeated' if part_occurence > 0 else ''}">
    <span class="part-name">${part_name}</span>
    % for chord in iter_chords(chart, part_name):
    <span class="bar">${u'—' if chord is None or part_occurence > 0 else render_chord(chord)}</span>
    % endfor
  </div>
  % endfor
</div>
% endif

<div class="form-actions">

  <div class="control-group">
    <div class="btn-group transpose-buttons" data-toggle="buttons-radio" title="Click to transpose chart in this key.">
% for key in common_chromatic_keys:
      <a class="${'active ' if key == chart.key else ''}btn"\
href="${request.route_path('chart', slug=chart.slug, _query=dict(key=key))}">\
  % if chart.default_key == key:
<strong>${key}</strong>
  % else:
${key}\
  % endif
</a>
% endfor
% if chart.key not in common_chromatic_keys:
      <a class="active btn"\
href="${request.route_path('chart', slug=chart.slug, _query=dict(key=chart.key))}">${chart.key}</a>
% endif
    </div>
  </div>

  <div class="control-group">
% if has_permission('edit', request.root, request):
    <a class="btn" href="${request.route_path('chart.edit', slug=chart.slug)}">Edit</a>
    <a class="btn" href="${request.route_path('chart.delete', slug=chart.slug)}">Delete</a>
% else:
    <a class="btn disabled" href="#" title="Login to edit this chart">Edit</a>
    <a class="btn disabled" href="#" title="Login to delete this chart">Delete</a>
% endif
    <a class="btn" href="${request.route_path('chart.json', slug=chart.slug, _query=dict(key=chart.key))}" \
title="Click to export this chart in JSON">Export in JSON</a>
  </div>

</div>

<%block filter="trim" name="footer">
<%include file="chart_footer.mako"/>
</%block>
