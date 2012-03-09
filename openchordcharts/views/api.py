# -*- coding: utf-8 -*-


# Open Chord Charts -- Database of free chord charts
# By: Christophe Benz <christophe.benz@gmail.com>
#
# Copyright (C) 2012 Christophe Benz
# https://gitorious.org/open-chord-charts/
#
# This file is part of Open Chord Charts.
#
# Open Chord Charts is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Open Chord Charts is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


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
