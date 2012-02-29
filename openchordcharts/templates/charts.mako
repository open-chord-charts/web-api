<%inherit file="site.mako"/>
<div class="page-header">
  <h1>Charts</h1>
</div>
<ul>
% for chart in charts:
  <li><a href="${request.route_path('chart', slug=chart.slug)}">${chart.title}</a></li>
% endfor
</ul>
