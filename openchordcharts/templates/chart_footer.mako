<%!
from babel.dates import format_datetime
%>

<p>
  Created by <a class="user" href="${request.route_path('user', slug=chart.user)}">${chart.user}</a>
  on ${format_datetime(chart.created_at)}.
</p>

% if chart.modified_at is not None and chart.modified_at != chart.created_at:
<p>
  Modified by <a class="user" href="${request.route_path('user', slug=chart.user)}">${chart.user}</a>
  on ${format_datetime(chart.created_at)}.
</p>
% endif
