import os
import unittest
import json

import settings
from todo_list.extensions import db
from todo_list.factory import create_app
from todo_list.models import Todo


class TodoTestCase(unittest.TestCase):

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
        response = self.client.get(
            '/api/todos/%d' % id,
            content_type='application/json')
        if response.status_code != 200:
            assert response.status_code == 404
            return None
        return json.loads(response.data)

    def list_all(self):
        response = self.client.get(
            '/api/todos/',
            content_type='application/json')
        if response.status_code != 200:
            assert response.status_code == 404
            return None
        return json.loads(response.data)


    def test_create(self):
        todo1 = self.create('Pick up kids')
        assert todo1['title'] == 'Pick up kids'
        assert todo1['order'] == 1
        assert not todo1['completed']

        todo2 = self.create('Buy groceries')
        assert todo2['title'] == 'Buy groceries'
        assert todo2['order'] == 2
        assert not todo2['completed']

        assert todo1['id'] != todo2['id']

    def test_read(self):
        todo = self.create('Pick up kids')

        read = self.read(todo['id'])

        assert read == todo

    def test_list(self):
        todo1 = self.create('Pick up kids')
        todo2 = self.create('Buy groceries')

        todos_list = self.list_all()
        todos = [todo1,todo2]
        assert todos_list['todos'] == todos

    def test_update(self):
        todo = self.create('Pick up kids')
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

