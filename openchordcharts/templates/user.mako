<%inherit file="site.mako"/>
<div class="page-header">
  <h1>My dashboard</h1>
</div>
<h2>My charts</h2>
<ul>
% for chart in user_charts:
  <li><a href="${request.route_path('chart', slug=chart.slug)}">${chart.title}</a></li>
% endfor
</ul>
