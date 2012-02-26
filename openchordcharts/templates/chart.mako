<%inherit file="site.mako"/>
<h2>${chart['properties']['title']}</h2>
<div class="properties">
    <h3>Properties</h3>
% if chart['properties'].get('compositors'):
    <div class="compositors">
        <p>Compositors:</p>
        <ul>
    % for compositor in chart['properties']['compositors']:
            <li>${compositor}</li>
    % endfor
        </ul>
    </div>
% endif
% if chart['properties'].get('genre'):
    <div class="genre">
        <p>Genre: <span class="genre">${chart['properties']['genre']}</span></p>
    </div>
% endif
% if chart['properties'].get('structure'):
    <div class="structure">
        <p>Structure: <span class="structure">${len(chart['chords'])} × ${''.join(chart['properties']['structure'])}</span></p>
    </div>
% endif
% if chart['properties'].get('tonality'):
    <div class="tonality">
        <p>Tonality: <span class="tonality">${chart['properties']['tonality']}</span></p>
    </div>
% endif
    <h3>Chords</h3>
    ${' '.join(chart['chords'])}
</div>
