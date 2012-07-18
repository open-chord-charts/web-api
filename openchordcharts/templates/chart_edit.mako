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


<%block name="article">
<div class="alert alert-block">
  <a class="close" data-dismiss="alert">×</a>
  <h4 class="alert-heading">Warning!</h4>
  <p>This form is still in development.</p>
  <p>You won't be able to save data if you use it!</p>
</div>

<form action="${form_action_url}" class="form-horizontal" method="post">
  <fieldset>
    <legend>Edit chart: ${chart_data.get('title')}</legend>

<%
error = chart_errors.get('title')
%>\
    <div class="control-group${' error' if error else ''}">
      <label class="control-label" for="title">Title</label>
      <div class="controls">
        <input class="input-xlarge" id="title" name="title" type="text" value="${chart_data.get('title')}">
% if error:
        <span class="help-inline">${error}</span>
% endif
      </div>
    </div>

<%
error = chart_errors.get('composers')
%>\
    <div class="control-group${' error' if error else ''}">
      <label class="control-label" for="composers">Composers</label>
      <div class="controls">
        <input class="input-xlarge" id="composers" name="composers" type="text"\
value="${', '.join(chart_data['composers'] if chart_data.get('composers') else '')}">
        <p class="help-block">Multiple values are comma-separated</p>
% if error:
        <span class="help-inline">${error}</span>
% endif
      </div>
    </div>

<%
error = chart_errors.get('genre')
%>\
    <div class="control-group${' error' if error else ''}">
      <label class="control-label" for="genre">Genre</label>
      <div class="controls">
        <input class="input-medium" id="genre" name="genre" type="text" value="${chart_data.get('genre')}">
% if error:
        <span class="help-inline">${error}</span>
% endif
        <p class="help-block">Examples: medium, etc.</p>
      </div>
    </div>

<%
error = chart_errors.get('structure')
%>\
    <div class="control-group${' error' if error else ''}">
      <label class="control-label" for="structure">Structure</label>
      <div class="controls">
        <input class="input-medium" id="structure" name="structure" type="text"\
value="${', '.join(chart_data['structure']) if chart_data.get('structure') else ''}">
% if error:
        <span class="help-inline">${error}</span>
% endif
        <p class="help-block">Examples: "A, A, B, A", "A, B, A, C", etc.</p>
      </div>
    </div>

<%
error = chart_errors.get('key')
%>\
    <div class="control-group${' error' if error else ''}">
      <label class="control-label" for="key">Key</label>
      <div class="controls">
        <select class="input-mini" id="key" name="key">
% for key in common_chromatic_keys:
          <option${' selected' if key == chart_data.get('key') else ''}>${key}</option>
% endfor
        </select>
% if error:
        <span class="help-inline">${error}</span>
% endif
        <p class="help-block">Default key for displaying chart.</p>
      </div>
    </div>
% if chart_data.get('structure'):
  % for part_name in sorted(set(chart_data['structure'])):
<%
error = chart_errors.get('parts.{0}'.format(part_name))
%>\
    <div class="control-group${' error' if error else ''}">
      <label class="control-label" for="part-${part_name}">Chords of part ${part_name}</label>
      <div class="controls">
        <textarea class="input-xlarge" id="part-${part_name}" name="parts.${part_name}" \
rows="${len(chart_data['parts'][part_name]) / 8 + 1}">${' '.join(chart_data['parts'][part_name])}</textarea>
  % if error:
        <span class="help-inline">${error}</span>
  % endif
      </div>
    </div>
  % endfor
% endif

    <div class="form-actions">
      <a class="btn" href="${cancel_url}" \
title="Click to cancel changes and go back to chart">Cancel</a>
      <button class="btn btn-primary" type="submit" title="Click to save changes">Save changes</button>
    </div>

  </fieldset>
</form>
</%block>


<%block name="title">
Edit "${chart.title}" - <%parent:title/>
</%block>
