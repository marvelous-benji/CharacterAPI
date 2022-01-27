from flask_migrate import Migrate

from project import create_app, db
from config import get_env
from project.models import User


app = create_app(get_env('FLASK_CONFIG'))


migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_processor():
    return dict(app=app, db=db, User=User)



if __name__ == '__main__':
    app.run()