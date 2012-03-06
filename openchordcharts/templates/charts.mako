<%inherit file="site.mako"/>
% if charts.count():
<ul>
  % for chart in charts:
  <li><a href="${request.route_path('chart', slug=chart.slug)}">${chart.title}</a></li>
  % endfor
</ul>
% else:
<p>No charts found.</p>
% endif
