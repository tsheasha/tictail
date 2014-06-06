/*global Backbone, jQuery, _, ENTER_KEY, ESC_KEY */
define([
  // These are path alias that we configured in our bootstrap
  'jquery',     // lib/jquery/jquery
  'underscore', // lib/underscore/underscore
  'backbone',    // lib/backbone/backbone
  'text!templates/todo/item.tpl'  
], function($, _, Backbone, TodoTemplate){
	'use strict';

	// Todo Item View
	// --------------

	// The DOM element for a todo item...
	var TodoView = Backbone.View.extend({
		//... is a list tag.
		tagName:  'li',

		// Cache the template function for a single item.
		template: _.template(TodoTemplate),

		// The DOM events specific to an item.
		events: {
			'click .toggle': 'toggleCompleted',
		},

		// The TodoView listens for changes to its model, re-rendering. Since there's
		// a one-to-one correspondence between a **Todo** and a **TodoView** in this
		// app, we set a direct reference on the model for convenience.
		initialize: function () {
			this.listenTo(this.model, 'change', this.render);
		},

		// Re-render the titles of the todo item.
		render: function () {
			// Backbone LocalStorage is adding `id` attribute instantly after creating a model.
			// This causes our TodoView to render twice. Once after creating a model and once on `id` change.
			// We want to filter out the second redundant render, which is caused by this `id` change.
			// It's known Backbone LocalStorage bug, therefore we've to create a workaround.
			// https://github.com/tastejs/todomvc/issues/469
			if (this.model.changed.id !== undefined) {
				return;
			}

			this.$el.html(this.template(this.model.toJSON()));
			this.$el.toggleClass('completed', this.model.get('completed'));
			return this;
		},


		// Toggle the `"completed"` state of the model.
		toggleCompleted: function () {
			this.model.toggle();
		},
	});
    return TodoView;
});
