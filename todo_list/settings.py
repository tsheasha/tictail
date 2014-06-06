import os

if 'DATABASE_URL' in os.environ:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    DEBUG = False
else:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///todos.db'
    DEBUG = True
