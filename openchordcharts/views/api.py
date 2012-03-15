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


from biryani.baseconv import cleanup_line
from biryani.strings import slugify
from pyramid.view import view_config

from openchordcharts.model.chart import Chart


@view_config(renderer='jsonp', route_name='charts.json')
def charts_json(request):
    spec = {}
    if request.GET.get('title'):
        title_slug = slugify(request.GET['title'])
        if title_slug:
            spec['keywords'] = Chart.get_search_by_keywords_spec(title_slug.split('-'))
    if request.GET.get('user'):
        user = cleanup_line(request.GET['user'])
        if user:
            spec['user'] = user
    return [chart.to_json() for chart in Chart.find(spec)]
