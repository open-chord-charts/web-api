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


<form class="form-horizontal" method="post">
  <fieldset>
    <legend>Login</legend>

<%
error = errors.get('email')
%>
    <div class="control-group${' error' if error else ''}">
      <label class="control-label" for="email">Email</label>
      <div class="controls">
        <input class="input-xlarge" id="email" name="email" type="text" value="${data.get('email')}">
% if error:
        <span class="help-inline">${error}</span>
% endif
      </div>
    </div>

<%
error = errors.get('password')
%>
    <div class="control-group${' error' if error else ''}">
      <label class="control-label" for="password">Password</label>
      <div class="controls">
        <input class="input-xlarge" id="password" name="password" type="text" value="${data.get('password')}">
% if error:
        <span class="help-inline">${error}</span>
% endif
      </div>
    </div>

    <div class="form-actions">
      <button class="btn btn-primary" type="submit">Login</button>
    </div>

  </fieldset>
</form>
