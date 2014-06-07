from extensions import db
from sqlalchemy.sql import func

class Todo(db.Model):
    """
    Todo Item database model defining 4 columns
        id: Integer field specifying primary key of row.
        title: String field specifying the todo item action.
        order: Integer field specifying the order of the todo item.
        completed: Boolean field specifying status of todo item.
        user_id: Foreign Key to User Model.
    """
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    order = db.Column(db.Integer)
    completed = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    
    # Transforms Model to JSON format
    def to_json(self):
    
        return {
                "id": self.id,
                "title": self.title,
                "order": self.order,
                "completed": self.completed,
                "user": self.user.username              
            }

    # Create new Model instance from JSON format
    def from_json(self, json_src):
        if 'title' in json_src:
            self.title = json_src['title']
        if 'order' in json_src:
            self.order = json_src['order']
        if 'completed' in json_src:
            self.completed = json_src['completed']
        self.save()

    # Create new Model instance from request.form format    
    # used when performing API calls.
    def from_form(self, form_src):
        if 'user_id' in form_src:
            self.user = User.query.filter_by(id=int(form_src['user_id'][0])).first()
        if 'title' in form_src:
            self.title = form_src['title'][0]
        if 'order' in form_src:
            self.order = int(form_src['order'][0])
        else:
            order = db.session.query(func.max(Todo.order) \
                                        .label("last_order")) \
                                    .one() \
                                    .last_order
            self.order = order + 1
        self.completed = False
        self.save()

    def save(self):
        db.session.add(self)
        db.session.commit()

class User(db.Model):
    """
    Todo Item database model defining 4 columns
        id: Integer field specifying primary key of row.
        username: String field specifying the user's username.
        password: Integer field specifying the password of the user.
        todos: One to Many realtionship with todo items.
    """
    __tablename__ = "users"
    id = db.Column('user_id',db.Integer , primary_key=True)
    username = db.Column('username', db.String(20), unique=True , index=True)
    password = db.Column('password' , db.String(10))
    todos = db.relationship('Todo' , backref='user',lazy='dynamic')
 
    def __init__(self , username ,password):
        self.username = username
        self.password = password
 
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)
 
    def __repr__(self):
        return '<User %r>' % (self.username)

    def save(self):
        db.session.add(self)
        db.session.commit()
