from models import Todo
from flask import Blueprint, jsonify, request, g
import json
from flask.ext.login import login_required, current_user


todo_blueprint = Blueprint('todos', __name__, url_prefix='/todos')

# List all Todos
@todo_blueprint.route('/', methods=['GET'])
@login_required
def list():
    todos = Todo.query.filter_by(user_id = g.user.id).order_by(Todo.order).all()
    todo_list = map(Todo.to_json, todos)
    return json.dumps(todo_list)

# Create new todo
@todo_blueprint.route('/', methods=['POST'])
@login_required
def create():
    todo = Todo()
    todo.user = g.user
    todo.from_json(request.get_json())
    return _todo_response(todo)

# Get a single todo item
@todo_blueprint.route('/<int:id>', methods=['GET'])
@login_required
def read(id):
    todo = Todo.query.get_or_404(id)
    return _todo_response(todo)

# Update order of todos
@todo_blueprint.route('/<int:id>', methods=['PUT', 'PATCH'])
@login_required
def update(id):
    todo = Todo.query.get_or_404(id)
    todo.from_json(request.get_json())
    return _todo_response(todo)

def _todo_response(todo):
    return jsonify(**todo.to_json())

@todo_blueprint.before_request
def before_request():
    g.user = current_user
