from flask import Blueprint, render_template, g
from flask.ext.login import login_required, current_user

# Creating an Index Blueprint in an effort to make the applicaiton Modular
index_blueprint = Blueprint('index', __name__)

# Render index.html template
@index_blueprint.route('/')
@login_required
def index():
    return render_template('index.html')

@index_blueprint.before_request
def before_request():
    g.user = current_user
