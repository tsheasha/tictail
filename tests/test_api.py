import os
import unittest
import json

from tests import settings
from todo_list.extensions import db
from todo_list.factory import create_app
from util import read, create, login, logout

class TodoAPITestCase(unittest.TestCase):

    def setUp(self):
        """
        Initialise Database with some values
        """
        self.app = create_app(
            priority_settings=settings)
    
        self.client = self.app.test_client()
        self.client.post('/register', data=dict(
            username='tsheasha',
            password='password'
        ))

        self.client.post('/register', data=dict(
            username='nahla',
            password='password'
        ))

        self.client.post('/login', data=dict(
            username='tsheasha',
            password='password'
        ))


        self.order = 1

    def tearDown(self):
        """
        Clear database
        """
        self.client.get('/logout')

        with self.app.app_context():
            db.drop_all()

    def test_create(self):
        """
        Test if API creates new todo item
        """
        todo = {"title": 'Write API tests',
                "order": self.order,
                "user_id":1}

        todo1 = create(self, url='/api', inp=todo)
        assert todo1['title'] == 'Write API tests'
        assert todo1['order'] == 1
        assert not todo1['completed']
        assert todo1['user'] == 'tsheasha'        

        todo = {"title": 'Write automation tests',
                "order": self.order,
                "user_id":1}

        todo2 = create(self, url='/api', inp=todo)
        assert todo2['title'] == 'Write automation tests'
        assert todo2['order'] == 2
        assert not todo2['completed']
        assert todo2['user'] == 'tsheasha'

        assert todo1['id'] != todo2['id']

        logout(self)
        login(self, "nahla", "password")
        
        todo = {"title": 'Write automation tests',
                "order": self.order,
                "user_id":2}
        
        todo3 = create(self, url='/api', inp=todo)
        assert todo3['title'] == 'Write automation tests'
        assert todo3['order'] == 3
        assert not todo3['completed']
        assert todo3['user'] == 'nahla'
    
    def test_read(self):
        """
        Test if API can get a single item by ID
        """
        todo = {"title": 'Write API tests',
                "order": self.order,
                "user_id":1}

        todo = create(self, url='/api', inp=todo)

        read1 = read(self, todo['id'], url='/api')

        assert read1 == todo

    def test_list(self):
        """
        Test if API returns list of all todos
        """
        todo = {"title": 'Write API tests',
                "order": self.order,
                "user_id":1}
        
        todo1 = create(self, url='/api', inp=todo)

        todo = {"title": 'Write automation tests',
                "order": self.order,
                "user_id":1}

        todo2 = create(self, url='/api', inp=todo)
        
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
        payload = {"title": 'Write API tests',
                "order": self.order,
                "user_id":1}

        todo = create(self, url='/api', inp=payload)
        id = todo['id']

        updates = {'order': 2}

        req = self.client.put(
            '/api/todos/%d' % id,
            data=updates,
            content_type='application/json')

        assert read(self, id, url='/api')['order'] == 2 
        assert req.status_code == 204 

if __name__ == '__main__':
    unittest.main()
