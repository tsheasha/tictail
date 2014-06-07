import os
import unittest
import json

from tests import settings
from todo_list.extensions import db
from todo_list.factory import create_app
from util import read, create, login, logout


class TodoTestCase(unittest.TestCase):

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
        Test if app creates new todo item
        """
        todo1 = create(self, 'Write app tests')
        assert todo1['title'] == 'Write app tests'
        assert todo1['order'] == 1
        assert not todo1['completed']
        assert todo1['user'] == 'tsheasha'

        todo2 = create(self,
            'Write automation tests', completed=True)
        assert todo2['title'] == 'Write automation tests'
        assert todo2['order'] == 2
        assert todo2['completed']
        assert todo2['user'] == 'tsheasha'

        logout(self)
        login(self, "nahla", "password")

        todo3 = create(self,
            'Write automation tests', completed=True)
        assert todo3['title'] == 'Write automation tests'
        assert todo3['order'] == 3
        assert todo3['completed']
        assert todo3['user'] == 'nahla'

    def test_read(self):
        """
        Test if app can get a single item by ID
        """
        todo1 = create(self, 'Write app tests')
        todo2 = create(self,
            'Write automation tests', completed=True)

        read1 = read(self, todo1['id'])
        read2 = read(self, todo2['id'])

        assert read1 == todo1
        assert read2 == todo2

        read3 = read(self, todo2['id'] + 1)
        assert read3 is None

    def test_list(self):
        """
        Test if app returns list of all todos
        """
        todo1 = create(self, 'Write app tests')
        todo2 = create(self,
            'Write automation tests', completed=True)

        response = self.client.get(
            '/todos/',
            content_type='application/json')
        if response.status_code != 200:
            assert response.status_code == 404
        
        todos_list = json.loads(response.data)

        todos = [todo1,todo2]
        assert todos_list == todos

    def test_update(self):
        """
        Test if app can update order of a todo item by ID
        """
        todo = create(self, 'Write app tests')
        id = todo['id']

        updates = dict(**todo)
        updates['completed'] = True
        updates['title'] = 'Write all app tests'

        req = self.client.put(
            '/todos/%d' % id,
            data=json.dumps(updates),
            content_type='application/json')
        updated = json.loads(req.data)

        assert updated == updates
        assert read(self, id) == updates

if __name__ == '__main__':
    unittest.main()
