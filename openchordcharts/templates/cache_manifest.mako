## Open Chord Charts -- Database of free chord charts
## By: Christophe Benz <christophe.benz@gmail.com>
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
<%!
from openchordcharts.helpers import get_git_revision
%>\
CACHE MANIFEST
# rev ${get_git_revision() or u'UNKNOWN!'}

CACHE:
${request.static_path('openchordcharts:static/fonts/lilyjazzchord.otf')}
${request.registry.settings['css.bootstrap']}
${request.registry.settings['css.bootstrap_responsive']}
${request.registry.settings['javascript.bootstrap']}
${request.registry.settings['bootstrap_dir']}/img/glyphicons-halflings.png
${request.registry.settings['bootstrap_dir']}/img/glyphicons-halflings-white.png
${request.registry.settings['javascript.jquery']}
${request.registry.settings['javascript.jqueryui']}
${request.registry.settings['javascript.spinejs_dir']}/spine.js
${request.static_path('openchordcharts:static/css/chart.css')}
${request.static_path('openchordcharts:static/css/style.css')}
${request.static_path('openchordcharts:static/js/chart.js')}
${request.static_path('openchordcharts:static/js/offline.js')}
${request.static_path('openchordcharts:static/templates/chart.js')}

FALLBACK:
/ /offline

NETWORK:
*
