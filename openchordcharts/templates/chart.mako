<%inherit file="site.mako"/>
<h2>${chart['title']}</h2>
<div class="properties">
    <h3>Properties</h3>
% if chart.get('compositors'):
    <div class="compositors">
        <p>Compositors:</p>
        <ul>
    % for compositor in chart['compositors']:
            <li>${compositor}</li>
    % endfor
        </ul>
    </div>
% endif
% if chart.get('genre'):
    <div class="genre">
        <p>Genre: <span class="genre">${chart['genre']}</span></p>
    </div>
% endif
% if chart.get('structure'):
    <div class="structure">
        <p>Structure: <span class="structure">${len(chart['chords'])} × ${''.join(chart['structure'])}</span></p>
    </div>
% endif
% if chart.get('key'):
    <div class="key">
        <p>Key: <span class="key">${chart['key']}</span></p>
    </div>
% endif
    <h3>Chords</h3>
    ${' '.join(chart['chords'])}
</div>
