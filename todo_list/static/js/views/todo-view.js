/*global Backbone, jQuery, _, ENTER_KEY, ESC_KEY */
define([
  'jquery',  
  'underscore',
  'backbone',
  'text!templates/todo/item.tpl'  
], function($, _, Backbone, TodoTemplate){
	'use strict';

	// Todo Item View
	// --------------

	var TodoView = Backbone.View.extend({
		
        tagName:  'li',

		// Cache the template function for a single item.
		template: _.template(TodoTemplate),

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
