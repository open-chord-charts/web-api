<%inherit file="site.mako"/>
<p>Charts list:</p>
<ul>
% for chart in charts:
    <li><a href="${request.route_path('chart', title=chart['properties']['title'])}">${chart['properties']['title']}</a></li>
% endfor
</ul>
