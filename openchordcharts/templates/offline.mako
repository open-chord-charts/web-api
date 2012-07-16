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


<%inherit file="site.mako"/>


<%block name="application_script">
$(function() {
  require("lib/setup");
  var offline = require("controllers/offline");
  this.offline = new offline.Offline({
    el: $(".content")
  });
});
</%block>


<%block name="article">
<div class="page-header">
  <h1>
    Offline
    <small>Use Open Chord Charts as an application.</small>
  </h1>
</div>
<div class="content">
  <div class="row">
    <p class="span9 status"></p>
  </div>
  <div class="progress-bar row">
    <p class="span1">Progress:</p>
    <div class="active progress progress-striped span6">
      <div class="bar" style="width: 0%;"></div>
    </div>
  </div>
  <button class="btn stop">Stop</button>
</div>
</%block>


<%block name="html_tag_opening">
<html manifest="${request.route_path('cache.manifest')}">
</%block>
