import os
import unittest
import json

from tests import settings
from todo_list.extensions import db
from todo_list.factory import create_app
from todo_list.models import Todo


class TodoAPITestCase(unittest.TestCase):

    def setUp(self):
        """
        Initialise Database with some values
        """
        self.app = create_app(
            priority_settings=settings)
    
        self.client = self.app.test_client()
        self.order = 1

    def tearDown(self):
        """
        Clear database
        """
        with self.app.app_context():
            db.drop_all()

    def create(self, title):
        """
        Create a new Todo item
        """
        todo = {"title": title,
                "order": self.order}
        response = self.client.post(
            '/api/todos/',
            data=todo)
        created = json.loads(response.data)

        assert 'id' in created
        assert created['title'] == title
        assert created['order'] == self.order
        assert created['completed'] == False
        assert response.status_code == 201
        self.order += 1

        return created

    def read(self, id):
        """
        Get a Todo item
        """
        response = self.client.get(
            '/api/todos/%d' % id,
            content_type='application/json')
        if response.status_code != 200:
            assert response.status_code == 404
            return None
        return json.loads(response.data)

    def test_create(self):
        """
        Test if API creates new todo item
        """

        todo1 = self.create('Write API tests')
        assert todo1['title'] == 'Write API tests'
        assert todo1['order'] == 1
        assert not todo1['completed']

        todo2 = self.create('Write automation tests')
        assert todo2['title'] == 'Write automation tests'
        assert todo2['order'] == 2
        assert not todo2['completed']

        assert todo1['id'] != todo2['id']

    def test_read(self):
        """
        Test if API can get a single item by ID
        """
        todo = self.create('Write API tests')

        read = self.read(todo['id'])

        assert read == todo

    def test_list(self):
        """
        Test if API returns list of all todos
        """
        todo1 = self.create('Write API tests')
        todo2 = self.create('Write automation tests')
        
        response = self.client.get(
            '/api/todos/',
            content_type='application/json')
        if response.status_code != 200:
            assert response.status_code == 404
        
        todos_list = json.loads(response.data)
        
        todos = [todo1,todo2]
        assert todos_list['todos'] == todos

    def test_update(self):
        """
        Test if API can update order of a todo item by ID
        """
        todo = self.create('Write API tests')
        id = todo['id']

        updates = {'order': 2}

        req = self.client.put(
            '/api/todos/%d' % id,
            data=updates,
            content_type='application/json')

        assert self.read(id)['order'] == 2 
        assert req.status_code == 204 

if __name__ == '__main__':
    unittest.main()

