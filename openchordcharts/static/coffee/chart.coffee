define ["jquery"], ($) ->

  initialize = (selector) ->
    $element = $(selector)
    $element.css
      "transform-origin": "top left"
      "-moz-transform-origin": "top left"
      "-webkit-transform-origin": "top left"
      transition: "transform 0.33s ease-in"
      "-moz-transition": "-moz-transform 0.33s ease-in"
      "-webkit-transition": "-webkit-transform 0.33s ease-in"
    $element.on "click", (event) ->
        scale = $element.parents(".container").width() / $element.width()
        marginBottom = $(selector).height() * (scale - 1)
        transformScale = "scale(" + scale + ")"
        $element.css
          "margin-bottom": marginBottom + parseInt($("p").css("margin-bottom"))
          transform: transformScale
          "-moz-transform": transformScale
          "-webkit-transform": transformScale

  initialize: initialize
