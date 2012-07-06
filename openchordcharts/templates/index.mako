## Open Chord Charts -- Database of free chord charts
## By: Christophe Benz <christophe.benz@gmail.com>
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


<%inherit file="site.mako"/>


<%block name="html_tag_opening">
% if data['appcache']:
<html manifest="${request.route_path('cache.manifest')}">
% else:
<html manifest="${request.route_path('cache.manifest', _query=dict(appcache=int(data['appcache'])))}">
% endif
</%block>


<div class="hero-unit">
  <p>
    The Open Chord Charts project aims to provide a database of music chord charts.
  </p>
  <ul>
    <li><p>For musicians, jazzmen in particular.</p></li>
    <li><p>Contribution is possible for everyone.</p></li>
    <li><p>Charts are published under Creative Commons licence (see below).</p></li>
  </ul>
  <p>
    <a class="btn btn-primary btn-large" href="${request.route_path('charts')}">View charts »</a>
  </p>
</div>

<div class="row">
  <div class="span4">
    <h2>Data</h2>
    <p>
      <span xmlns:dct="http://purl.org/dc/terms/" href="http://purl.org/dc/dcmitype/Dataset" property="dct:title" rel="dct:type">Open Chord Charts data</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="http://www.openchordcharts.org/" property="cc:attributionName" rel="cc:attributionURL">http://www.openchordcharts.org/</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/">Creative Commons Attribution-ShareAlike 3.0 Unported License</a>.
    </p>
    <p>
      <a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/">
        <img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by-sa/3.0/88x31.png" />
      </a>
    </p>
    <p>
      This means that everyone can view, modify, reuse data and contribute to the projet freely (as in free software).
    </p>
    <p>
      Also webservices and data exports are available for communication with external applications (for programmers!).
    </p>
    <p>
      Data is published under the contributors resposibility.
    </p>
  </div>
  <div class="span4">
    <h2>Software</h2>
    <p>
      The software running this website is published under the
      <a href="http://www.gnu.org/licenses/agpl.html">GNU Affero General Public License</a>.
    </p>
    <p>
      Get its <a href="https://gitorious.org/open-chord-charts/">source code</a> from the git repository at gitorious.
    </p>
  </div>
  <div class="span4">
    <h2>Contact</h2>
    <p>Main developer: <a href="mailto:christophe.benz@gmail.com">christophe.benz@gmail.com</a></p>
  </div>
</div>
