<%inherit file="site.mako"/>

<%
is_own_user_page = request.user and request.user.slug == request.matchdict.get('slug')
%>

<div class="page-header">
  <h1>${'My' if is_own_user_page else request.matchdict.get('slug')} charts</h1>
</div>

% if user_charts.count():
<ul>
  % for chart in user_charts:
  <li><a href="${request.route_path('chart', slug=chart.slug)}">${chart.title}</a></li>
  % endfor
</ul>
% else:
<p>
  % if is_own_user_page:
  You have not created any chart. You can browse <a href="${request.route_path('charts')}">all the charts</a> from the project.
  % else:
  This user has not created any chart.
  % endif
</p>
% endif
