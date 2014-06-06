from todo_list.models import Todo
from flask import Blueprint, jsonify, request
import json

api_todo_blueprint = Blueprint('api', __name__, url_prefix='/api/todos')

# API call to list all Todos
@api_todo_blueprint.route('/', methods=['GET'])
def list():
    todos = Todo.query
    if 'limit' in request.args:
        todos = todos.limit(int(request.args['limit']))
    else:
        todos = todos.limit(50)
    if 'offset' in request.args:
        todos = todos.offset(int(request.args['offset']))  
    todos = todos.all()
    todo_list = map(Todo.to_json, todos)
    return jsonify(todos=todo_list), 200

# API call to create new Todo
@api_todo_blueprint.route('/', methods=['POST'])
def create():
    todo = Todo()
    todo.from_form(dict(request.form))
    return _todo_response(todo), 201

# API call to get a single Todo
@api_todo_blueprint.route('/<int:id>', methods=['GET'])
def read(id):
    todo = Todo.query.get_or_404(id)
    return _todo_response(todo), 200

# API call to update order of Todos
@api_todo_blueprint.route('/<int:id>', methods=['PUT', 'PATCH'])
def update(id):
    todo = Todo.query.get_or_404(id)
    todo.from_form(dict(request.form))
    return _todo_response(todo), 204

def _todo_response(todo):
    return jsonify(**todo.to_json())
