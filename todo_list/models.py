from extensions import db
from sqlalchemy.sql import func

class Todo(db.Model):
    """
    Todo Item database model defining 4 columns
        id: Integer field specifying primary key of row.
        title: String field specifying the todo item action.
        order: Integer field specifying the order of the todo item.
        completed: Boolean field specifying status of todo item.
    """
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    order = db.Column(db.Integer)
    completed = db.Column(db.Boolean)
    
    # Transforms Model to JSON format
    def to_json(self):
    
        return {
                "id": self.id,
                "title": self.title,
                "order": self.order,
                "completed": self.completed
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
