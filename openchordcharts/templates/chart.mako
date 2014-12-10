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
import json

from babel.dates import format_datetime
from pyramid.security import has_permission

from openchordcharts.helpers import get_login_url
from openchordcharts.utils import common_chromatic_keys
%>


<%block name="script_domready">
<%parent:script_domready/>
require("bootstrapify");
$("*[rel~='popover']").popover({
  placement: "bottom"
});
var chart = new window.openchordcharts.Charts({
  chart: ${json.dumps(dict(
    key=chart.key,
    parts=chart.parts,
    slug=chart.slug,
    structure=chart.structure,
    title=chart.title,
  )) | n},
  el: $("body")
});
##  $(".chords").draggable({
##    axis: "y",
##    handle: ".part-name",
##    revert: true
##  });
</%block>


<%block name="title">
${u'{0} ({1})'.format(chart.title, chart.key)} - <%parent:title/>
</%block>


% if chart.is_deleted and has_permission('edit', request.root, request):
<div class="alert alert-block">
  <a class="close" data-dismiss="alert">×</a>
  <h4 class="alert-heading">Warning!</h4>
  <p>This chart is marked as deleted.</p>
  <p><a class="btn" href="${request.route_path('chart.undelete', slug=slug)}">Undelete</a></p>
</div>
% endif

<div class="actions">
## Previous versions of chart in history do not provide edit and delete buttons.
% if not data['revision']:
  % if has_permission('edit', request.root, request):
  <a class="btn" href="${request.route_path('chart.edit', slug=slug)}">Edit</a>
    % if not chart.is_deleted:
  <a class="btn delete" href="${request.route_path('chart.delete', slug=slug)}">Delete</a>
    % endif
  % else:
  <a class="btn" data-content="Edition is restricted to authenticated users." href="${get_login_url(request)}" \
rel="nofollow popover" title="Please login first!">Edit</a>
    % if not chart.is_deleted:
  <a class="btn" data-content="Deletion is restricted to authenticated users." href="${get_login_url(request)}" \
rel="nofollow popover" title="Please login first!">Delete</a>
    % endif
  % endif
% endif
  <a class="btn" href="${request.route_path('chart.history', slug=slug)}">History</a>
  <a class="btn" href="${request.route_path('chart.json', slug=slug, _query=dict(
    key=chart.key,
    revision=data['revision'] or '',
    ))}" \
rel="external" title="Get JSON version of this chart (for programmers)">Raw data</a>
</div>

<div class="page-header">
  <h1>
    <span class="title">${chart.title}</span>
% if chart.composers:
    <small class="composers">${u', '.join(chart.composers)}</small>
% endif
  </h1>
</div>

% if data['revision']:
<div class="alert alert-block">
  <a class="close" data-dismiss="alert">×</a>
  <h4 class="alert-heading">Previous version!</h4>
  <p>This chart is a previous version modified at ${format_datetime(chart.modified_at)}).</p>
  <p><a class="btn" href="${request.route_path('chart', slug=slug)}">Current version</a></p>
</div>
% endif

<div class="properties">
  <div class="left">
% if chart.structure:
    <span class="structure">${len(list(chart.iter_chords()))} × ${''.join(chart.structure)}</span>
% endif
% if chart.genre:
    <span class="genre">${chart.genre}</span>
% endif
  </div>

  <div class="key right">
    <form method="get">
      <select class="input-mini" name="key" title="Transpose chart into another key">
% for key in common_chromatic_keys:
        <option${u' selected' if key == chart.key else ''} value="${key}">\
${u'{0}{1}'.format(key, u' (original)' if key == original_key else '')}</option>
% endfor
% if chart.key not in common_chromatic_keys:
        <option selected value="${chart.key}">${chart.key}</option>
% endif
      </select>
      <input class="btn" type="submit" value="Transpose">
    </form>
  </div>
</div>

<div class="chords">
% if chart.structure:
  <table class="table table-bordered table-striped">
    <tbody>
  % for part_name in chart.structure:
<%
part_nb_lines = len(chart.parts[part_name]) / 8
%>
      <tr>
        <td class="part-name"${u' rowspan="{0}"'.format(part_nb_lines) if part_nb_lines > 1 else '' | n}>
          ${part_name}
        </td>
    % for chord_index, chord in enumerate(chart.parts[part_name]):
      % if chord_index % 8 == 0 and chord_index != 0:
      <tr>
      % endif
        <td class="bar">${chord}</td>
    % endfor
      </tr>
  % endfor
    </tbody>
  </table>
% endif
</div>

<%block name="footer">
<%include file="chart_footer.mako"/>
</%block>
