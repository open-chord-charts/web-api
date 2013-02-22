<%inherit file='/site.mako' />


<%block name="container_content">
<div class="hero-unit">
  <h1>Open Chord Charts</h1>
  <p class="muted">Share the chords of your favorite songs!</p>
  <p>A chart represents the chords of a song. Wanna play a tune? Get its chord chart!</p>
  <a class="btn btn-primary btn-large charts" href="/charts">View charts »</a>
</div>

<div class="row">
  <div class="span4">
    <h2>Open Data</h2>
    <p>
      Everyone can contribute to the projet by adding its own charts.
    </p>
    <p>
      Charts are shared publically but edition is restricted to owners.
    </p>
    <p>
      We provide an HTTP API for application developers.
    </p>
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
  </div>
  <div class="span4">
    <h2>Free Software</h2>
    <p>
      The source code of the software running this website is published under the
      <a href="http://www.gnu.org/licenses/agpl.html" rel="external">GNU Affero General Public License</a>.
    </p>
    <p>
      <a href="https://gitorious.org/open-chord-charts/" rel="external">Get it on gitorious!</a>
    </p>
  </div>
  <div class="span4">
    <h2>Contact</h2>
    <p>
      The Open Chord Charts developers:
      <a href="mailto:contact@openchordcharts.org" rel="external">contact@openchordcharts.org</a>
    </p>
  </div>
</div>
</%block>
