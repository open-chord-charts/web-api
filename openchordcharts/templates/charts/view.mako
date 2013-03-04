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
from babel.dates import format_datetime
from markupsafe import Markup

from openchordcharts import chart_render, music_theory
%>


<%inherit file="/site.mako"/>


<%block name="container_content">
<div class="page-header">
  <h1>
    <span class="title">${chart.title}</span>
% if chart.composers:
    <small class="composers">${u', '.join(chart.composers)}</small>
% endif
  </h1>
</div>

<div class="properties">
% if chart.genre or chart.structure:
  <div class="row">
  % if chart.structure:
    <div class="span2">
      <span class="structure">${u', '.join(chart.structure)}</span>
    </div>
  % endif
  % if chart.genre:
    <div class="span10">
      <span class="genre">${chart.genre}</span>
    </div>
  % endif
  </div>
% endif

  <div class="key row">
    <div class="span2">
      Key: ${chart.key}
    </div>
    <div class="span10">
      <div class="btn-toolbar">
        <div class="btn-group" data-toggle="buttons-radio">
% for key in music_theory.common_chromatic_keys:
<%
is_active_key = data['key'] is None and key == chart.key or key == data['key']
%>
          <a class="${'active ' if is_active_key else ''}btn${' original-key' if key == chart.key else ''}" \
href="?key=${key}">
            ${key}
          </a>
% endfor
        </div>
      </div>
    </div>
  </div>
</div>

% if chart.structure:
<div class="chords">
  <table class="table table-bordered table-striped">
    <tbody>
    % for part in chart_render.build_parts(chart, chords_per_row=8, from_key=chart.key, to_key=data['key']):
        % for row_index, row in enumerate(part['rows']):
      <tr>
            % if row_index == 0:
        <td class="part-name"${u' rowspan="{0}"'.format(len(part['rows'])) if len(part['rows']) > 1 else '' | n}>
          ${part['name']}
        </td>
            % endif
            % for cell in row:
        <td class="bar">${cell}</td>
            % endfor
      </tr>
        % endfor
    % endfor
    </tbody>
  </table>
</div>
% endif

<%
user = req.ctx.find_user()
%>
% if user is not None and user._id == chart.account_id:
<div class="btn-toolbar">
  <a class="btn edit" href="/charts/${chart.slug}/edit">Edit</a>
  <a class="btn delete" href="/charts/${chart.slug}/delete">Delete</a>
</div>
% endif

% if chart.modified_at != chart.created_at:
<p>
  Last modified on ${format_datetime(chart.modified_at)}
  % if chart_owner is not None:
  by <a class="user" href="/users/${chart_owner.slug}">${chart_owner.slug}</a>
  % endif
</p>
% endif

<p>
  Created on ${format_datetime(chart.created_at)}
% if chart_owner is not None:
  by <a class="user" href="/users/${chart_owner.slug}">${chart_owner.slug}</a>
% endif
</p>
</%block>


<%block name="domready_content">
$('a.delete').on('click', function(evt) {
  if ( ! confirm('Delete this chart?')) {
    evt.preventDefault();
  }
});
</%block>
