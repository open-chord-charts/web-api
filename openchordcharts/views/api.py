# -*- coding: utf-8 -*-

import re

from biryani.strings import slugify
from pyramid.view import view_config

from openchordcharts.model.chart import Chart


@view_config(route_name='charts.json', renderer='jsonp')
def charts_json(request):
    title = request.GET.get('title')
    user = request.GET.get('user')
    spec = {}
    if title:
        title_words = slugify(title).split('-')
        title_words_regexps = [re.compile(u'^{0}'.format(re.escape(word))) for word in title_words]
        spec['keywords'] = {'$all': title_words_regexps}
    if user:
        spec['user'] = user
    return [chart.to_json() for chart in Chart.find(spec)]
