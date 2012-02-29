<%inherit file="site.mako"/>

<%def name="css()" filter="trim">
<%parent:css/>
<link href="/static/css/chart.css" rel="stylesheet">
</%def>

<div class="page-header">
  <h1>
    ${chart.title}
% if chart.compositors:
    <small class="compositors">${', '.join(chart.compositors)}</small>
% endif
  </h1>
</div>
<div class="properties">
% if chart.genre:
  <div class="genre">
    <p>Genre: <span class="genre">${chart.genre}</span></p>
  </div>
% endif
% if chart.structure:
  <div class="structure">
    <p>Structure: <span class="structure">${len(chart.chords)} × ${''.join(chart.structure)}</span></p>
  </div>
% endif
% if chart.key:
  <div class="key">
    <p>Key: <span class="key">${chart.key}</span></p>
  </div>
% endif
  <div class="chords">
% for part in chart.structure:
    <div class="part">
      <span class="part-name">${part}</span>
    % for chord in chart.get_part_chords(part):
      <span class="bar">${chord}</span>
    % endfor
    </div>
% endfor
  </div>
</div>
