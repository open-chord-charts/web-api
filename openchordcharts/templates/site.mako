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


<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="description" content="Open Chord Charts project">
    <meta name="author" content="Christophe Benz">
    <title><%block name="title">Open Chord Charts</%block></title>
    <link rel="stylesheet" href="${ctx.conf['cdn.bootstrap.css']}">
    <link href="/css/lilyjazzchord.css" rel="stylesheet">
    <link href="/style.css" rel="stylesheet">
   </head>
  <body>

    <%include file="navbar.mako"/>

    <div class="container">
      <%block name="container_content" />
    </div>

    <div class="container">
      <hr>
      <p>Copyright © The Open Chord Charts contributors, 2012-2013</p>
    </div>

    <script src="${ctx.conf['cdn.jquery.js']}"></script>
    <script src="${ctx.conf['cdn.bootstrap.js']}"></script>
    <script>
% if ctx.conf['google_analytics_key'] is not None:
var _gaq = _gaq || [];
_gaq.push(['_setAccount', '${ctx.conf['google_analytics_key']}']);
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
