/*global Backbone */
define([
  'backbone'  
], function(Backbone){
    	'use strict';

	// Todo Model
	// ----------

	// **Todo** model has `title`, `order`, and `completed` attributes.
	var Todo = Backbone.Model.extend({
		// Default attributes for the todo
		// and ensure that each todo created has `title`, `todo_id`, and `completed` keys.
		defaults: {
            todo_id: '',
			title: '',
			completed: false,
		},
        
		// Toggle the `completed` state of this todo item.
		toggle: function () {
			this.save({
				completed: !this.get('completed')
			});
		}
	});
    return Todo;
});

