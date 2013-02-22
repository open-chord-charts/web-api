function initOpenChordCharts() {
  var $ul = $('ul.charts');
  if ($ul && document.body.clientWidth <= 979) {
    transformListLinksIntoBlockButtons({$el: $ul});
  }
  $('a[rel="external"]').attr('target', '_blank');
}


function transformListLinksIntoBlockButtons(options) {
  options.$el.addClass('unstyled');
  $('li a', options.$el).each(function(idx, item) {
    $(item)
      .addClass('btn btn-block btn-large mobile-list-item')
      .append($('<i>', {'class': 'icon-chevron-right pull-right'}));
  });
}
