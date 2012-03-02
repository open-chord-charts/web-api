require.config
  baseUrl: "/static"
  paths:
    # Dependencies
    bootstrap: "lib/bootstrap-2.0.1/js/bootstrap.min"
    jquery: "lib/jquery-1.7.1.min"
    use: "lib/requirejs-1.0.7/use"
  use:
    bootstrap:
      deps: ["jquery"]


require ["use!bootstrap"], (_bootstrap) ->
