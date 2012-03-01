<%inherit file="site.mako"/>

<%def name="css()" filter="trim">
<%parent:css/>
<link href="/static/css/chart.css" rel="stylesheet">
</%def>

<%def name="scripts()" filter="trim">
<script>
require(["chart"], function(chart) {
  chart.initialize(".chords");
});
</script>
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
  <p>Structure: <span class="structure">${len(chart.chords)} × ${''.join(chart.structure)}</span></p>
% endif
% if chart.key:
  <p>Key: <span class="key">${chart.key}</span></p>
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
% if request.session.get('user_email'):
  <p>Added by <a class="user" href="${request.route_path('user', user_email=chart.user)}">${chart.user}</a></p>
% endif
</div>
