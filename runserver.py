from todo_list.factory import create_app
import os

if 'DATABASE_URL' in os.environ:
    application = create_app()
else:
    app = create_app()
    app.run()

