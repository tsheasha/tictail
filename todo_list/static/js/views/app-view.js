/*global Backbone, jQuery, _, ENTER_KEY */
var ENTER_KEY = 13;

define([
  'jquery',
  'jqueryui', 
  'underscore',
  'backbone',
  'views/todo-view',
  'collections/todos',
  'text!templates/todo/stats.tpl'
], function($, ui, _, Backbone, TodoView, Todos, StatsTemplate){
	'use strict';

	// The Application
	// ---------------

	// **AppView** is the top-level piece of UI.
	var AppView = Backbone.View.extend({

		el: '#todoapp',

		// Template for the line of statistics at the bottom of the app.
		statsTemplate: _.template(StatsTemplate),

		// Delegated events for creating new items.
		events: {
			'keypress #new-todo': 'createOnEnter',
			'click #toggle-all': 'toggleAllComplete'
		},

		// At initialization bind to the relevant events on the `Todos`
		// collection, when items are added or changed. Kick things off by
		// loading any preexisting todos that might be saved in *localStorage*.
		initialize: function () {
			this.allCheckbox = this.$('#toggle-all')[0];
			this.$input = this.$('#new-todo');
			this.$footer = this.$('#footer');
			this.$main = this.$('#main');
			this.$list = $('#todo-list');

            this.todos = new Todos();
            this.todos.url = '/todos/';      
            var todos = this.todos; 
            
            // Making the Todo Items sortable.
            this.$("#todo-list").sortable({
                update: function(event, ui) {
                    $('div.view',this).each(function(i){
                        var id = $(this).attr('data-id'),
                            todo = todos.get(parseInt(id));
                        todo.save({order: i + 1});
                    });
                }
            });
                              
			this.listenTo(this.todos, 'add', this.addOne);
			this.listenTo(this.todos, 'reset', this.addAll);
			this.listenTo(this.todos, 'change:completed', this.filterOne);
			this.listenTo(this.todos, 'all', this.render);

            this.todos.fetch();
		},

		// Re-rendering the App just means refreshing the statistics -- the rest
		// of the app doesn't change.
		render: function () {
			var completed = this.todos.completed().length;
			var remaining = this.todos.remaining().length;

			if (this.todos.length) {
				this.$main.show();
				this.$footer.show();

				this.$footer.html(this.statsTemplate({
					completed: completed,
					remaining: remaining
				}));

			} else {
				this.$main.hide();
				this.$footer.hide();
			}

			this.allCheckbox.checked = !remaining;
            return this;
		},

		// Add a single todo item to the list by creating a view for it, and
		// appending its element to the `<ul>`.
		addOne: function (todo) {
			var view = new TodoView({ model: todo });
			this.$list.append(view.render().el);
		},

		// Add all items in the **Todos** collection at once.
		addAll: function () {
			this.$list.html('');
			this.todos.each(this.addOne, this);
		},


		// Generate the attributes for a new Todo item.
		newAttributes: function () {
			return {
                todo_id: $("li").size() + 1,
				title: this.$input.val().trim(),
				order: this.todos.nextOrder(),
				completed: false
			};
		},

		// If you hit return in the main input field, create new **Todo** model
		createOnEnter: function (e) {
			if (e.which === ENTER_KEY && this.$input.val().trim()) {
				this.todos.create(this.newAttributes());
				this.$input.val('');
			}
		},

		toggleAllComplete: function () {
			var completed = this.allCheckbox.checked;

			this.todos.each(function (todo) {
				todo.save({
					'completed': completed
				});
			});
		}
	});
    return AppView;
});
