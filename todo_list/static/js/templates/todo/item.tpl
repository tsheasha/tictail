<div class="view" data-id="<% if (todo_id) { %><%= todo_id %><% } else { %> <%= id %><% } %>">
    <input class="toggle" type="checkbox" <%= completed ? 'checked' : '' %>>
    <label><%- title %></label>
    <button class="sort"></button>
</div>
