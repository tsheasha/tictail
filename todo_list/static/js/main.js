/*global $ */
/*jshint unused:false */
var ENTER_KEY = 13;
var ESC_KEY = 27;

require.config({ 
    baseUrl: 'js',
    paths: {
        jquery: 'libs/jquery/jquery',
        jqueryui: 'libs/jquery/jquery-ui',
        underscore: 'libs/underscore/underscore',
        backbone: 'libs/backbone/backbone',
        views: 'views',
        models: 'models',
        templates: 'templates',
        collections: 'collections',
    },
 
    shim: {
        'underscore': {
            exports: '_'
        },
      'backbone': {
            deps: ['underscore', 'jquery'],
            exports: 'Backbone'
        },
        "jquery-ui": {
            exports: "$",
            deps: ['jquery']
        },
    }
});

require([

  // Load our app module and pass it to our definition function
  'app',
], function(App){
  // The "app" dependency is passed in as "App"
  App.initialize();
});
