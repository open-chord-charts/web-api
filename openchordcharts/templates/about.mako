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


<%block name="title">
<%parent:title/>: About
</%block>


<div class="hero-unit">
  <h2>Presentation</h2>
  <p>
    This project is targeted for musicians. It aims to create a database of chord charts from scratch, in a crowdsourcing way.
  </p>
  <p><a class="btn btn-primary btn-large" href="${request.route_path('charts')}">Browse charts »</a></p>
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
      Webservices and data exports are available for communication with external applications.
    </p>
    <p>
      Data is published under the contributors resposibility.
    </p>
  </div>
  <div class="span4">
    <h2>Software</h2>
    <p>
      This is a free software published under the
      <a href="http://www.gnu.org/licenses/agpl.html">GNU Affero General Public License</a>.
    </p>
    <p>
      Get the <a href="https://gitorious.org/open-chord-charts/">source code</a> from the git repository.
    </p>
  </div>
  <div class="span4">
    <h2>Contact</h2>
    <p>Main developer: <a href="mailto:christophe.benz@gmail.com">christophe.benz@gmail.com</a></p>
  </div>
</div>
