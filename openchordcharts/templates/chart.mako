<%inherit file="site.mako"/>

<%!
from openchordcharts.helpers import iter_chords, iter_structure, render_chord
from openchordcharts.utils import all_keys
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

<div class="properties">
% if chart.genre:
  <p>Genre: <span class="genre">${chart.genre}</span></p>
% endif
% if chart.structure:
  <p>Structure: <span class="structure">${len(list(chart.iter_chords()))} × ${''.join(chart.structure)}</span></p>
% endif

  <form action="${request.route_path('chart', slug=chart.slug)}" class="well form-inline">
    <label for="key">Key:</label>
    <select class="key" id="key" name="key">
% for key, offset in all_keys:
      <option ${'selected' if key == chart.key else ''}>${key}</option>
% endfor
    </select>
    <button class="btn transpose">Transpose</button>
  </form>

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

% if request.session.get('user_email'):
  <p>Added by <a class="user" href="${request.route_path('user', user_email=chart.user)}">${chart.user}</a></p>
% endif
</div>
