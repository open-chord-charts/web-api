<!DOCTYPE html>
<%block name="html_tag_opening">
<html>
</%block>

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
import json

from openchordcharts.conv import user_to_json_dict
%>


  <head>
    <meta charset="utf-8">
    <meta name="description" content="Open Chord Charts project">
    <meta name="author" content="Christophe Benz">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1, maximum-scale=1.0, \
user-scalable=0">
    <title>OpenChordCharts.org</title>
    <link href="${request.static_path('openchordcharts:static/bootstrap-2.0.4/css/bootstrap{0}.css'.format(
'' if request.registry.settings['development_mode'] else '.min'))}" rel="stylesheet">
    <style>
      body {
        padding-top: 60px;
        padding-bottom: 40px;
      }
    </style>
    <link href="${request.static_path('openchordcharts:static/bootstrap-2.0.4/css/bootstrap-responsive{0}.css'.format(
'' if request.registry.settings['development_mode'] else '.min'))}" rel="stylesheet">
    <link href="${request.static_path('openchordcharts:static/application.css')}" rel="stylesheet">
   </head>
  <body>

    <%include file="navbar.mako"/>

    <div class="container">
      <article>
        ${eco_template | n}
      </article>
      <footer>
        <hr>
        <p>Copyright © The Open Chord Charts contributors, 2012</p>
        <p class="application-cache-info"></p>
        <p class="navigator-info"></p>
      </footer>
    </div>

    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"></script>
    <script src="${request.static_path('openchordcharts:static/bootstrap-2.0.4/js/bootstrap{0}.js'.format(
'' if request.registry.settings['development_mode'] else '.min'))}"></script>
    <script src="${request.static_path('openchordcharts:static/application.js')}"></script>
    <script>
$(function() {
  var index = require("index");
  this.app = new index.App({
    el: $("body"),
    user: ${json.dumps(user_to_json_dict(request.user) if request.user else None) | n}
  });
});

% if request.registry.settings['google.analytics.key']:
var _gaq = _gaq || [];
_gaq.push(['_setAccount', '${request.registry.settings['google.analytics.key']}']);
_gaq.push(['_trackPageview']);
(function() {
  var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
  ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
  var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
})();
% endif
    </script>
  </body>
</html>
