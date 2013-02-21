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


<%!
from babel.dates import format_datetime

from openchordcharts import chord_helpers
from openchordcharts.model.chart import common_chromatic_keys
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
  <div class="left">
% if chart.structure:
    <span class="structure">${u', '.join(chart.structure)}</span>
% endif
% if chart.genre:
    <span class="genre">${chart.genre}</span>
% endif
  </div>

  <div class="key right">
    <select class="input-mini" name="key" title="Transpose chart into another key">
% for key in common_chromatic_keys:
      <option${' selected' if key == chart.key else ''} value="${key}">${key}</option>
% endfor
% if chart.key not in common_chromatic_keys:
      <option selected value="${chart.key}">${chart.key}</option>
% endif
    </select>
  </div>
</div>

% if chart.structure:
<div class="chords">
  <table class="table table-bordered table-striped">
    <tbody>
    % for part in chord_helpers.render_parts(chart):
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

<div class="btn-toolbar">
<%
user = req.ctx.user
%>
% if user is not None and user._id == chart.account_id:
  <a class="btn edit" href="/charts/${chart.slug}/edit">Edit</a>
% endif
</div>

% if chart.modified_at != chart.created_at:
<p>
  Last modified on ${format_datetime(chart.modified_at)}
  % if chart_account_slug is not None:
  by <a class="user" href="/users/${chart_account_slug}">${chart_account_slug}</a>
  % endif
</p>
% endif

<p>
  Created on ${format_datetime(chart.created_at)}
% if chart_account_slug is not None:
  by <a class="user" href="/users/${chart_account_slug}">${chart_account_slug}</a>
% endif
</p>
</%block>
