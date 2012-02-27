<%inherit file="site.mako"/>
<p>Charts list:</p>
<ul>
% for chart in charts:
    <li><a href="${request.route_path('chart', slug=chart.slug)}">${chart.title}</a></li>
% endfor
</ul>
