from flask import Flask

from . import settings
from extensions import db 
from index import index_blueprint
from todo import todo_blueprint
from api.v1.todo import api_todo_blueprint

from flask.ext.heroku import Heroku
from flask.ext.compress import Compress

def create_app(priority_settings=None):
    
    # Initialising a Flask App
    app = Flask(__name__, static_url_path='')
    heroku = Heroku()
    compress = Compress() 

    app.config.from_object(priority_settings)
    # Load configuraiton from settings file
    app.config.from_object(settings)

    # Initialise database
    db.init_app(app)

    # Using Heroku as deployment server
    heroku.init_app(app)
    
    # Gziping responses from app
    compress.init_app(app)

    # Registering Blueprints in an effor to make app modular
    app.register_blueprint(index_blueprint)
    app.register_blueprint(todo_blueprint)
    app.register_blueprint(api_todo_blueprint)

    with app.app_context():
        db.create_all()
    return app
