/*global $ */
/*jshint unused:false */

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
    // Shim these dependcies to define order to requireJS's asynchronous feature 
    shim: {
        'underscore': {
            exports: '_'
        },
        'jqueryui': {
            exports: "$",
            deps: ['jquery']
        },
        'backbone': {
            deps: ['underscore', 'jquery'],
            exports: 'Backbone'
        }
    }
});

require([

  // Load our app module and pass it to our definition function
  'app',
], function(App){
  // The "app" dependency is passed in as "App"
  App.initialize();
});
