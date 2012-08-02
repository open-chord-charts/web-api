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
from openchordcharts.helpers import get_revision_hash
%>\
CACHE MANIFEST
# rev ${get_revision_hash() or u'UNKNOWN!'}

CACHE:
//ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js
${request.static_path('openchordcharts:static/fonts/lilyjazzchord-webfont.eot')}
${request.static_path('openchordcharts:static/fonts/lilyjazzchord-webfont.svg')}
${request.static_path('openchordcharts:static/fonts/lilyjazzchord-webfont.woff')}
${request.static_path('openchordcharts:static/bootstrap-2.0.4/css/bootstrap{0}.css'.format(
'' if request.registry.settings['development_mode'] else '.min'))}
${request.static_path('openchordcharts:static/bootstrap-2.0.4/css/bootstrap-responsive{0}.css'.format(
'' if request.registry.settings['development_mode'] else '.min'))}
${request.static_path('openchordcharts:static/bootstrap-2.0.4/img/glyphicons-halflings.png')}
${request.static_path('openchordcharts:static/bootstrap-2.0.4/img/glyphicons-halflings-white.png')}
${request.static_path('openchordcharts:static/bootstrap-2.0.4/js/bootstrap{0}.js'.format(
'' if request.registry.settings['development_mode'] else '.min'))}
${request.static_path('openchordcharts:static/css/lilyjazzchord.css')}
${request.static_path('openchordcharts:static/application.css')}
${request.static_path('openchordcharts:static/application.js')}

FALLBACK:
/ /

NETWORK:
*
