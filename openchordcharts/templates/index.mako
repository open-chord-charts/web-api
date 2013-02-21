<%inherit file='/site.mako' />


<%block name="container_content">
<div class="hero-unit">
  <h1>Open Chord Charts</h1>
  <ul>
    <li><p>For musicians</p></li>
    <li><p>Contribution is opened to everyone</p></li>
    <li><p>Data is published under a Creative Commons licence</p></li>
  </ul>
  <p>
    <a class="btn btn-large" href="http://en.wikipedia.org/wiki/Chord_chart" rel="external">What is a chord chart?</a>
    <a class="btn btn-primary btn-large charts" href="/charts">View charts »</a>
  </p>
</div>

<div class="row">
  <div class="span4">
    <h2>Data</h2>
    <p>
      <span xmlns:dct="http://purl.org/dc/terms/" href="http://purl.org/dc/dcmitype/Dataset" property="dct:title"
rel="dct:type external">Open Chord Charts data</span> by <a xmlns:cc="http://creativecommons.org/ns#"
href="http://www.openchordcharts.org/" property="cc:attributionName" rel="cc:attributionURL external">
http://www.openchordcharts.org/</a> is licensed under a <a rel="external license"
href="http://creativecommons.org/licenses/by-sa/3.0/">Creative Commons Attribution-ShareAlike 3.0 Unported License</a>.
    </p>
    <p>
      <a rel="external license" href="http://creativecommons.org/licenses/by-sa/3.0/">
        <img alt="Creative Commons License" style="border-width:0"
src="http://i.creativecommons.org/l/by-sa/3.0/88x31.png" />
      </a>
    </p>
    <p>
      Everyone can view, modify, reuse data and contribute to the projet freely (as in free software).
    </p>
    <p>
      Webservices and raw data exports are available for communication with external applications
      (for programmers!).
    </p>
    <p>
      Data is published under the contributors resposibility.
    </p>
  </div>
  <div class="span4">
    <h2>Software</h2>
    <p>
      The software running this website is published under the
      <a href="http://www.gnu.org/licenses/agpl.html" rel="external">GNU Affero General Public License</a>.
    </p>
    <p>
      Get its <a href="https://gitorious.org/open-chord-charts/" rel="external">source code</a> from the git repository
      at gitorious.
    </p>
    <a href="http://www.w3.org/html/logo/">
    <img src="http://www.w3.org/html/logo/badge/html5-badge-h-css3-semantics-storage.png" width="197" height="64"
alt="HTML5 Powered with CSS3 / Styling, Semantics, and Offline &amp; Storage"
title="HTML5 Powered with CSS3 / Styling, Semantics, and Offline &amp; Storage">
    </a>
  </div>
  <div class="span4">
    <h2>Contact</h2>
    <p>
      Main developer: Christophe Benz
      <a href="mailto:christophe.benz@gmail.com" rel="external">christophe.benz@gmail.com</a>
    </p>
  </div>
</div>
</%block>
