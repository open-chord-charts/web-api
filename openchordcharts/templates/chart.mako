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

from openchordcharts.helpers.chords import iter_rendered_chords, iter_parts_and_occurences, render_chord
from openchordcharts.utils import common_chromatic_keys
%>


<%block name="css">
<%parent:css/>
<link href="/static/css/chart.css" rel="stylesheet">
</%block>


<%block name="title">
${u'{0} ({1})'.format(chart.title, chart.key)} - <%parent:title/>
</%block>


% if chart.is_deleted and has_permission('edit', request.root, request):
<div class="alert alert-block">
  <a class="close" data-dismiss="alert">×</a>
  <h4 class="alert-heading">Warning!</h4>
  <p>This chart is marked as deleted.</p>
  <a class="btn" href="${request.route_path('chart.undelete', slug=chart.slug)}">Undelete</a>
</div>
% endif

<div class="page-header">
  <h1>
    <span class="title">${chart.title}</span>
% if chart.composers:
    <small class="composers">${u', '.join(chart.composers)}</small>
% endif
  </h1>
</div>

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
<table class="chords table table-bordered table-striped">
  <tbody>
  % for part_name, part_occurence in iter_parts_and_occurences(chart):
<%
part_rendered_chord = list(iter_rendered_chords(chart, part_name))
part_nb_lines = len(part_rendered_chord) / 8
%>
    <tr>
      <td class="part-name"${u' rowspan="{0}"'.format(part_nb_lines) if part_nb_lines > 1 else '' | n}>
        ${part_name}
      </td>
    % for chord_index, chord in enumerate(part_rendered_chord):
      % if chord_index % 8 == 0 and chord_index != 0:
    <tr>
      % endif
      <td class="bar">${u'—' if chord is None or part_occurence > 0 else render_chord(chord)}</td>
    % endfor
    </tr>
  % endfor
  </tbody>
</table>
% endif

<div class="form-actions">

  <div class="control-group">
    <div class="btn-group transpose-buttons" data-toggle="buttons-radio" title="Click to transpose chart in this key.">
% for key in common_chromatic_keys:
      <a class="${'active ' if key == chart.key else ''}btn"\
href="${request.route_path('chart', slug=chart.slug, _query=dict(key=key))}">\
  % if original_key == key:
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
  % if not chart.is_deleted:
    <a class="btn" href="${request.route_path('chart.delete', slug=chart.slug)}">Delete</a>
  % endif
% else:
    <a class="btn disabled" href="#" title="Login to edit this chart">Edit</a>
  % if not chart.is_deleted:
    <a class="btn disabled" href="#" title="Login to delete this chart">Delete</a>
  % endif
% endif
    <a class="btn" href="${request.route_path('chart.json', slug=chart.slug, _query=dict(key=chart.key))}" \
title="Click to export this chart in JSON">Export in JSON</a>
  </div>

</div>

<%block name="footer">
<%include file="chart_footer.mako"/>
</%block>
