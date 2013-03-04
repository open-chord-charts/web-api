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


function disableSubmitWhenEnterKeyPressed(options) {
  $('input', options.$el).on('keypress', function(evt) {
    if (evt.keyCode == 13) {
      // Enter key pressed.
      evt.preventDefault();
    }
  });
}


function transformSelectIntoToolbar(options) {
  var $select = $('select', options.$el);
  $select.remove();
  var $btnGroup = $('<div>', {'class': 'btn-group', 'data-toggle': 'buttons-radio'});
  var $hiddenInput = $('<input>', {'name': options.name, 'type': 'hidden'});
  $('option', $select).each(function(idx, item) {
    var $option = $(item);
    var optionVal = $option.val();
    if (optionVal) {
      var $button = $('<button>', {'class': 'btn', 'text': optionVal})
        .on('click', function (evt) {
          evt.preventDefault();
          $hiddenInput.val($(evt.currentTarget).text());
        })
        .appendTo($btnGroup);
      if ($option.is(':selected')) {
        $button.addClass('active');
        $hiddenInput.val(optionVal);
      }
    }
  });
  options.$el
    .prepend($btnGroup)
    .prepend($hiddenInput);
}
