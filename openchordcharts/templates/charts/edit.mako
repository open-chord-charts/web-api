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
from webhelpers.html import tags
%>


<%inherit file="/site.mako"/>


<%block name="container_content">
<div class="page-header">
  <h1>Edit "${chart.title}"</h1>
</div>

<form class="edit form-horizontal" method="post">
% if errors:
  <div class="alert alert-error">
    <strong>Fix errors!</strong> Some fields contain invalid values.
  </div>
% endif
  <fieldset>
    <%self:control_group key="title" label="Title" value="${inputs.get('title')}" />
    <%self:control_group key="composers" label="Composers" value="${inputs.get('composers')}" />
    <%self:control_group key="genre" label="Genre" value="${inputs.get('genre')}" />
    <%self:control_group key="structure" label="Structure" value="${inputs.get('structure')}" />
% for part_name, chords in inputs.get('parts').iteritems():
    <div class="control-group${' error' if errors.get('parts', {}).get(part_name) else ''}">
      <label class="control-label" for="part-${part_name}">Chords of part ${part_name}</label>
      <div class="controls">
        <div class="textarea">
          <textarea class="input-xxlarge" id="part-${part_name}" name="part.${part_name}">${chords}</textarea>
% if errors.get('parts', {}).get(part_name):
          <span class="help-block">
            <span class="label label-important">Error${u's' if len(errors['parts'][part_name]) > 1 else ''}</span>
              ${tags.ul(u'#{0} ({1}): {2}'.format(idx, data['parts'][part_name][idx], message)
                for idx, message in errors['parts'][part_name].iteritems())}
          </span>
% endif
        </div>
      </div>
    </div>
% endfor
    <div class="form-actions">
      <a class="btn cancel" href="/charts/${chart.slug}">Cancel</a>
      <input class="btn btn-primary" type="submit" value="Save">
    </div>
  </fieldset>
</form>
</%block>


<%def name="control_group(key, label, value)">
<div class="control-group${' error' if errors.get(key) else ''}">
  <label class="control-label" for="${key}">${label}</label>
  <div class="controls">
    <input class="input-xxlarge" id="${key}" name="${key}" type="text" value="${value}">
% if errors.get(key):
    <span class="help-inline"><span class="label label-important">Error</span> ${errors[key]}</span>
% endif
  </div>
</div>
</%def>
