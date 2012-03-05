<%inherit file="site.mako"/>
<div class="page-header">
% if request.session.get('user_email') == request.matchdict.get('user_email'):
  <h1>My charts</h1>
% else:
  <h1>${request.matchdict.get('user_email')} charts</h1>
% endif
</div>

<ul>
% for chart in user_charts:
  <li><a href="${request.route_path('chart', slug=chart.slug)}">${chart.title}</a></li>
% endfor
</ul>
