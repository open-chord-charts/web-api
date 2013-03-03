/*
Open Chord Charts -- Database of free chord charts
By: Christophe Benz <contact@openchordcharts.org>

Copyright (C) 2012-2013 Christophe Benz
https://gitorious.org/open-chord-charts/

This file is part of Open Chord Charts.

Open Chord Charts is free software; you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

Open Chord Charts is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/


function initOpenChordCharts() {
  var $ul = $('ul.charts');
  if ($ul && document.body.clientWidth <= 979) {
    transformListLinksIntoBlockButtons({$el: $ul});
  }
  $('a[rel="external"]').attr('target', '_blank');
}


function transformListLinksIntoBlockButtons(options) {
  var $buttonGroup = $('<div>', {'class': 'btn-group btn-group-vertical mobile-list'});
  $('li a', options.$el).each(function(idx, item) {
    $(item)
      .addClass('btn btn-block btn-large')
      .append($('<i>', {'class': 'icon-chevron-right pull-right'}))
      .appendTo($buttonGroup);
  });
  options.$el.replaceWith($buttonGroup)
}
