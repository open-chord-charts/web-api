# From http://stackoverflow.com/questions/7156218/how-to-implement-array-any-and-array-all-methods-in-coffeescript

Array.prototype.some ?= (f) ->
  (return true if f x) for x in @
  return false

Array.prototype.every ?= (f) ->
  (return false if not f x) for x in @
  return true
