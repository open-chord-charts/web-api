<%inherit file="site.mako"/>
<div class="page-header">
% if request.session.get('user_email') == request.matchdict.get('user_email'):
  <h1>My dashboard</h1>
% else:
  <h1>${request.matchdict.get('user_email')}</h1>
% endif
</div>

% if request.session.get('user_email') == request.matchdict.get('user_email'):
<h2>My charts</h2>
% else:
<h2>User charts</h2>
% endif

<ul>
% for chart in user_charts:
  <li><a href="${request.route_path('chart', slug=chart.slug)}">${chart.title}</a></li>
% endfor
</ul>
