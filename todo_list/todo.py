from models import Todo
from flask import Blueprint, jsonify, request
import json

todo_blueprint = Blueprint('todos', __name__, url_prefix='/todos')

# List all Todos
@todo_blueprint.route('/', methods=['GET'])
def list():
    todos = Todo.query.order_by(Todo.order).all()
    todo_list = map(Todo.to_json, todos)
    return json.dumps(todo_list)

# Create new todo
@todo_blueprint.route('/', methods=['POST'])
def create():
    todo = Todo()
    todo.from_json(request.get_json())
    return _todo_response(todo)

# Get a single todo item
@todo_blueprint.route('/<int:id>', methods=['GET'])
def read(id):
    todo = Todo.query.get_or_404(id)
    return _todo_response(todo)

# Update order of todos
@todo_blueprint.route('/<int:id>', methods=['PUT', 'PATCH'])
def update(id):
    todo = Todo.query.get_or_404(id)
    todo.from_json(request.get_json())
    return _todo_response(todo)

def _todo_response(todo):
    return jsonify(**todo.to_json())
