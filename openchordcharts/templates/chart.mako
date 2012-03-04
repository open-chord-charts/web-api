<%inherit file="site.mako"/>

<%!
from openchordcharts.helpers import render_chord
%>

<%def name="css()" filter="trim">
<%parent:css/>
<link href="/static/css/chart.css" rel="stylesheet">
</%def>

<div class="page-header">
  <h1>
    <span class="title">${chart.title}</span>
% if chart.compositors:
    <small class="compositors">${', '.join(chart.compositors)}</small>
% endif
  </h1>
</div>
<div class="properties">
% if chart.genre:
  <p>Genre: <span class="genre">${chart.genre}</span></p>
% endif
% if chart.structure:
  <p>Structure: <span class="structure">${chart.get_nb_chords()} × ${''.join(chart.structure)}</span></p>
% endif
% if chart.key:
  <p>Key: <span class="key">${chart.key}</span></p>
% endif
  <div class="chords">
% for part_name, part_occurence in chart.iter_structure():
    <div class="part\
  % if part_occurence > 0:
 repeated\
  % endif
">
      <span class="part-name">${part_name}</span>
  % for chord in chart.iter_chords(part_name):
      <span class="bar">
  % if part_occurence > 0:
        —
  % else:
        ${render_chord(chord)}
  % endif
      </span>
  % endfor
    </div>
% endfor
  </div>
% if request.session.get('user_email'):
  <p>Added by <a class="user" href="${request.route_path('user', user_email=chart.user)}">${chart.user}</a></p>
% endif
</div>
