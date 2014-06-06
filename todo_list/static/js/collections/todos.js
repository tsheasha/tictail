/*global Backbone */
define([
  'backbone',    
  'models/todo'
], function(Backbone, Todo){
	'use strict';

	// Todo Collection
	// ---------------

	var Todos = Backbone.Collection.extend({
		// Reference to this collection's model.
		model: Todo,

		// Filter down the list of all todo items that are finished.
		completed: function () {
			return this.filter(function (todo) {
				return todo.get('completed');
			});
		},

		// Filter down the list to only todo items that are still not finished.
		remaining: function () {
			return this.without.apply(this, this.completed());
		},

        // Find order to be chosen for next todo item
		nextOrder: function () {
			if (!this.length) {
				return 1;
			}
			return this.last().get('order') + 1;
		},

		comparator: function (todo) {
			return todo.get('order');
		}
	});

	return Todos;
});
