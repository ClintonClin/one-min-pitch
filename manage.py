from . import create_app, db
from flask_script import Manager, Server
from models import User, Pitch, Comment
from flask_migrate import Migrate, MigrateCommand


# Creating app instance
# calling the create app function and passing in the configuration_options keys so as to create the app instance
app = create_app('development')


manager = Manager(app)  # instantiate Manager class by passing app instance
# create command line argument to tell us how to run the app. add_command method to create new command 'server' which will launch the app server
manager.add_command('server', Server)

# initialize Migrate class and pass in app instance & db SQLAlchemy instance.
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.shell  # creation of a shellcontext
def make_shell_context():  # function allows us to pass properties into the shell.
    # returning of the app instance, db instance and User class
    return dict(app=app, db=db, User=User, Pitch=Pitch, Comment=Comment)


if __name__ == '__main__':
    manager.run()
