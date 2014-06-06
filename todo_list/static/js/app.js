/*global $ */
/*jshint unused:false */

define([
  'jquery',
  'underscore',
  'backbone',
  'views/app-view', // Request app-view.js
], function($, _, Backbone, AppView){
  var initialize = function(){
    // Initialise our AppView module
    new AppView();
  }

  return {
    initialize: initialize
  };
});
