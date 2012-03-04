<%inherit file="site.mako"/>
<div class="page-header">
  <h1>Charts</h1>
</div>
% if charts.count():
<ul>
  % for chart in charts:
  <li><a href="${request.route_path('chart', slug=chart.slug)}">${chart.title}</a></li>
  % endfor
</ul>
% else:
<p>No charts found.</p>
% endif
