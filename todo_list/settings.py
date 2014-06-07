import os

SECRET_KEY = '\xb5|\xe1T+\xea\x90\xc3E\xbf\xe4\xe1\xc9\x02A\xacSk@Xq.\x90\xd2'

if 'DATABASE_URL' in os.environ:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    DEBUG = False
else:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///todos.db'
    DEBUG = True
