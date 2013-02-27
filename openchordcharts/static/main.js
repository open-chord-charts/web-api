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
