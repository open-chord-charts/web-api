<%!
from openchordcharts.helpers import get_git_revision
%>\
CACHE MANIFEST
# rev ${get_git_revision() or u'UNKNOWN!'}
${request.static_path('openchordcharts:static/fonts/lilyjazzchord.otf')}
${request.registry.settings['css.bootstrap']}
${request.registry.settings['css.bootstrap_responsive']}
${request.registry.settings['javascript.bootstrap']}
${request.registry.settings['javascript.jquery']}
${request.registry.settings['javascript.jqueryui']}
${request.registry.settings['javascript.spinejs_dir']}/spine.js
${request.static_path('openchordcharts:static/css/chart.css')}
${request.static_path('openchordcharts:static/css/style.css')}
${request.static_path('openchordcharts:static/js/chart.js')}
${request.static_path('openchordcharts:static/js/offline.js')}
${request.static_path('openchordcharts:static/templates/chart.js')}
