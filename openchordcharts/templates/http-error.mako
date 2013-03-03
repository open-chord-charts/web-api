## -*- coding: utf-8 -*-


## Open Chord Charts -- Database of free chord charts
## By: Christophe Benz <contact@openchordcharts.org>
##
## Copyright (C) 2012 Christophe Benz
## https://gitorious.org/open-chord-charts/
##
## This file is part of Open Chord Charts.
##
## Open Chord Charts is free software; you can redistribute it and/or modify
## it under the terms of the GNU Affero General Public License as
## published by the Free Software Foundation, either version 3 of the
## License, or (at your option) any later version.
##
## Open Chord Charts is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Affero General Public License for more details.
##
## You should have received a copy of the GNU Affero General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.


<%inherit file="/site.mako"/>


<%block name="container_content">
<div class="alert alert-block alert-error">
  <h4 class="alert-heading">${title}</h4>
  <p>${explanation}</p>
% if comment:
  <p>${comment}</p>
% endif
% if message:
  <p>${message}</p>
% endif
% if dump:
    % if isinstance(dump, basestring):
  <pre class="break-word">${dump}</pre>
    % else:
  <pre class="break-word">${pprint.pformat(dump).decode('utf-8')}</pre>
    % endif
% endif
</div>
</%block>


<%block name="title_content">
${title} - ${parent.title_content()}
</%block>
