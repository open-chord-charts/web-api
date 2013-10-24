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
import collections

from webhelpers.html import tags

from openchordcharts import music_theory
%>


<%inherit file="/site.mako"/>


<%block name="container_content">
<div class="page-header">
% if req.path.endswith('/create'):
  <h1>Create a new chart</h1>
% else:
  <h1>Edit "${chart.title}"</h1>
% endif
</div>

<form class="edit form-horizontal" method="post">
  <div class="alert alert-info">
    Fields with an asterix (*) are mandatory.
  </div>
% if errors:
  <div class="alert alert-error">
    <strong>Fix errors!</strong> Some fields contain invalid values.
  </div>
% endif
  <fieldset>
    <%self:control_group label="Title (*)" name="title" value="${inputs.get('title')}" />
    <div class="control-group${' error' if errors.get('key') else ''}">
      <label class="control-label" for="key">Key (*)</label>
      <div class="controls key">
        <select class="input-mini" name="key">
          <option value="">--</option>
% for key in music_theory.common_chromatic_keys:
          <option${' selected' if inputs.get('key') is not None and inputs['key'] == key else ''} value="${key}">
            ${key}
          </option>
% endfor
        </select>
% if errors.get('key'):
        <span class="help-inline"><span class="label label-important">Error</span> ${errors['key']}</span>
% endif
      </div>
    </div>
    <%self:control_group label="Composers" name="composers" value="${inputs.get('composers')}" />
    <%self:control_group label="Genre" name="genre" value="${inputs.get('genre')}" />

  <div class="control-group${' error' if errors.get('structure') else ''}">
    <label class="control-label" for="structure">Structure</label>
    <div class="controls">
      <input class="input-xxlarge" id="structure" name="structure" type="text" value="${inputs.get('structure') or ''}">
% if errors.get('structure'):
<%
error_label = u'Error'
if isinstance(errors['structure'], collections.Mapping):
  if len(errors['structure']) > 1:
    error_label = u'Errors'
  error_message = u', '.join(
    u'{0}: {1}'.format(part_name, errors['structure'][part_name].lower()) for part_name in sorted(errors['structure'])
    )
else:
  error_message = errors['structure']
%>
      <span class="help-inline"><span class="label label-important">${error_label}</span> ${error_message}</span>
% endif
    </div>
  </div>
% if inputs.get('parts'):
  % for part_name in sorted(inputs['parts'], key=lambda item: inputs['structure'].index(item)):
    <div class="control-group${' error' if errors.get('parts', {}).get(part_name) else ''}">
      <label class="control-label" for="part-${part_name}">Chords of part ${part_name}</label>
      <div class="controls">
        <div class="textarea">
          <textarea class="input-xxlarge" id="part-${part_name}" name="part.${part_name}">\
${inputs['parts'][part_name]}</textarea>
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
% endif
    <div class="form-actions">
      <a class="btn cancel" href="/users/${req.ctx.user.username}/charts/\
${'' if req.path.endswith('/create') else chart.slug}">Cancel</a>
      <input class="btn btn-primary" type="submit" value="Save">
    </div>
  </fieldset>
</form>
</%block>


<%def name="control_group(label, name, value)">
<div class="control-group${' error' if errors.get(name) else ''}">
  <label class="control-label" for="${name}">${label}</label>
  <div class="controls">
    <input class="input-xxlarge" id="${name}" name="${name}" type="text" value="${value or ''}">
% if errors.get(name):
    <span class="help-inline"><span class="label label-important">Error</span> ${errors[name]}</span>
% endif
  </div>
</div>
</%def>


<%block name="page_scripts">
<script src="/charts/edit.js"></script>
<script>
$(function() {
  disableSubmitWhenEnterKeyPressed({
    $el: $('form.edit')
  });
});
</script>
</%block>
