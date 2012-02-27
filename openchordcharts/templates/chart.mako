<%inherit file="site.mako"/>
<%def name="css()" filter="trim">
<link href="/static/css/chart.css" rel="stylesheet">
</%def>\
<h2>${chart.title}</h2>
<div class="properties">
    <h3>Properties</h3>
% if chart.compositors:
    <div class="compositors">
        <p>Compositors:</p>
        <ul>
    % for compositor in chart.compositors:
            <li>${compositor}</li>
    % endfor
        </ul>
    </div>
% endif
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
    <h3>Chords</h3>
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
