<%inherit file="site.mako"/>

<%!
from babel.dates import format_datetime

from openchordcharts.helpers import iter_chords, iter_structure, render_chord
from openchordcharts.utils import common_chromatic_keys
%>

<%def name="css()" filter="trim">
<%parent:css/>
<link href="/static/css/chart.css" rel="stylesheet">
</%def>

<div class="page-header">
  <h1>
    <span class="title">${chart.title}</span>
% if chart.compositors:
    <small class="compositors">${u', '.join(chart.compositors)}</small>
% endif
  </h1>
</div>

<form action="${request.route_path('chart', slug=chart.slug)}">
  <div class="btn-group" data-toggle="buttons-radio" title="Click to transpose chart in this key.">
% for key in common_chromatic_keys:
    <button class="${'active ' if key == chart.key else ''}btn" name="key" value="${key}">${key}</button>
% endfor
% if chart.key not in common_chromatic_keys:
    <button class="active btn" name="key" value="${chart.key}">${chart.key}</button>
% endif
  </div>
</form>

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

<div class="chords">
% for part_name, part_occurence in iter_structure(chart):
  <div class="part ${'repeated' if part_occurence > 0 else ''}">
    <span class="part-name">${part_name}</span>
  % for chord in iter_chords(chart, part_name):
    <span class="bar">${u'—' if chord is None or part_occurence > 0 else render_chord(chord)}</span>
  % endfor
  </div>
% endfor
</div>

<%block filter="trim" name="footer">
<p>
  Created by <a class="user" href="${request.route_path('user', user_email=chart.user)}">${chart.user}</a>
  on ${format_datetime(chart.created_at)}.
</p>

% if chart.modified_at is not None and chart.modified_at != chart.created_at:
<p>
  Modified by <a class="user" href="${request.route_path('user', user_email=chart.user)}">${chart.user}</a>
  on ${format_datetime(chart.created_at)}.
</p>
% endif
</%block>
