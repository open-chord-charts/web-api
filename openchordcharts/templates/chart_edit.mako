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
from openchordcharts.utils import common_chromatic_keys
%>

<div class="alert alert-block">
  <a class="close" data-dismiss="alert">×</a>
  <h4 class="alert-heading">Warning!</h4>
  <p>This form is still in development.</p>
  <p>You won't be able to save data if you use it!</p>
</div>

<form action="${request.route_path('chart.edit', slug=chart.slug)}" class="form-horizontal" method="post">
  <fieldset>
    <legend>Edit chart: ${chart.title}</legend>
    <div class="control-group">
      <label class="control-label" for="title">Title</label>
      <div class="controls">
        <input class="input-xlarge" id="title" name="title" type="text" value="${chart.title}">
      </div>
    </div>
    <div class="control-group">
      <label class="control-label" for="composers">Composers</label>
      <div class="controls">
        <input class="input-xlarge" id="composers" name="composers" type="text" value="${', '.join(chart.composers)}">
        <p class="help-block">Multiple values are comma-separated</p>
      </div>
    </div>
    <div class="control-group">
      <label class="control-label" for="key">Key</label>
      <div class="controls">
        <select class="input-mini" id="key" name="key">
% for key in common_chromatic_keys:
          <option${' selected' if key == chart.key else ''}>${key}</option>
% endfor
        </select>
        <p class="help-block">Default key for displaying chart.</p>
      </div>
    </div>
    <div class="control-group">
      <label class="control-label" for="genre">Genre</label>
      <div class="controls">
        <input class="input-medium" id="genre" name="genre" type="text" value="${chart.genre}">
        <p class="help-block">Examples: medium, etc.</p>
      </div>
    </div>
    <div class="control-group">
      <label class="control-label" for="structure">Structure</label>
      <div class="controls">
        <input class="input-medium" id="structure" name="structure" type="text" value="${''.join(chart.structure)}">
        <p class="help-block">Examples: AABA, ABAC, etc.</p>
      </div>
    </div>
% for part_name in sorted(set(chart.structure)):
    <div class="control-group">
      <label class="control-label" for="chords">Chords of part ${part_name}</label>
      <div class="controls">
        <textarea class="input-xlarge" id="chords-${part_name}" name="chords.${part_name}" \
rows="${len(chart.parts[part_name]) / 8 + 1}"> ${' '.join(chart.parts[part_name])}</textarea>
      </div>
    </div>
% endfor
    <div class="form-actions">
      <a class="btn" href="${request.route_path('chart', slug=chart.slug)}" title="Click to cancel changes and go back to chart">Cancel</a>
      <button class="btn btn-primary" type="submit" title="Click to save changes">Save changes</button>
    </div>
  </fieldset>
</form>

<%block filter="trim" name="footer">
<%include file="chart_footer.mako"/>
</%block>
