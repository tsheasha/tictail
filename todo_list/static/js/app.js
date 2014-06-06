/*global $ */
/*jshint unused:false */

define([
  'jquery',
  'underscore',
  'backbone',
  'views/app-view', // Request app-view.js
], function($, _, Backbone, AppView){
  var initialize = function(){
    // Pass in our AppView module and initialize it
    new AppView();
  }

  return {
    initialize: initialize
  };
});
