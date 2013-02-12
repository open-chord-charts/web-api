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


<%block name="container_content">
<div class="page-header">
  <h1>
    Edit <span class="title">${chart.title}</span>
  </h1>
</div>

<form class="edit form-horizontal">
  <fieldset>
    <div class="control-group">
      <label class="control-label" for="title">Title</label>
      <div class="controls">
        <input class="input-xlarge" id="title" name="title" type="text" value="${chart.title}">
        <span class="help-inline"></span>
      </div>
    </div>
    <div class="control-group">
      <label class="control-label" for="composers">Composers</label>
      <div class="controls">
        <input class="input-xlarge" id="composers" name="composers" type="text"
          value="${u', '.join(chart.composers) if chart.composers else ''}">
        <span class="help-inline"></span>
      </div>
    </div>
    <div class="control-group">
      <label class="control-label" for="genre">Genre</label>
      <div class="controls">
        <input class="input-xlarge" id="genre" name="genre" type="text" value="${chart.genre}">
        <span class="help-inline"></span>
      </div>
    </div>
    <div class="control-group">
      <label class="control-label" for="structure">Structure</label>
      <div class="controls">
        <input class="input-xlarge" id="structure" name="structure" type="text"
          value="${u', '.join(chart.structure) if chart.structure else ''}">
        <span class="help-inline"></span>
      </div>
    </div>
% for part_name, chords in chart.parts.iteritems():
    <div class="control-group">
      <label class="control-label">Chords of part ${part_name}</label>
      <div class="controls">
        <div class="textarea">
          <textarea class="input-xlarge">${u' '.join(chords) if chords else ''}</textarea>
          <span class="help-inline"></span>
        </div>
      </div>
    </div>
% endfor
    <div class="form-actions">
      <button class="btn btn-primary">Save</button>
      <a class="btn cancel" href="/charts/${chart.slug}">Cancel</a>
    </div>
  </fieldset>
</form>


% if chart.structure:
<div class="chords">
  <table class="table table-bordered table-striped">
    <tbody>
    % for part in chart.parts:
        % for row_index, row in enumerate(part.rows):
      <tr>
            % if row_index == 0:
        <td class="part-name"${u' rowspan="{0}"'.format(len(part.rows)) if len(part.rows) > 1 else '' | n}>
          ${part.name}
        </td>
            % endif
            % for chord in row:
        <td class="bar">${chord}</td>
            % endfor
      </tr>
        % endfor
    % endfor
    </tbody>
  </table>
</div>
% endif
</%block>
