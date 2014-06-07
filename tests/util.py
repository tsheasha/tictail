import os
import unittest
import json

from tests import settings
from todo_list.extensions import db
from todo_list.factory import create_app

def create(self, title='', completed=False, url='', inp=None):
    """
    Create a new Todo item
    """
    ctype=None
    if not inp:
        todo = {"title": title,
                "order": self.order,
                "completed": completed}
        inp = json.dumps(todo)
        ctype = 'application/json'

    if not title:
        title = inp['title']
         
    response = self.client.post(
        url + '/todos/',
        data=inp,
        content_type=ctype)
    created = json.loads(response.data)

    assert 'id' in created
    assert created['title'] == title
    assert created['order'] == self.order
    assert created['completed'] == completed
    assert response.status_code == 201
    
    self.order += 1

    return created

def read(self, id, url=''):
    """
    Get a Todo item
    """
    ctype = 'application/json'
    if not url:
        ctype = None
    
    response = self.client.get(
        url + '/todos/%d' % id,
        content_type=ctype)

    if response.status_code != 200:
        assert response.status_code == 404
        return None
    return json.loads(response.data)

def login(self, username, password):
    """
    Login client given credentials
    """
    return self.client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def logout(self):
    """
    Logout currently logged in client.
    """
    self.client.get('/logout')
