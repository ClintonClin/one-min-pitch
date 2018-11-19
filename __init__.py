
from flask import Flask  # import the Flask class from the flask module
from flask_bootstrap import Bootstrap
from .config import config_options  # import config_options from the config file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_simplemde import SimpleMDE
from flask_mail import Mail

login_manager = LoginManager()  # creation of an instance of the class
# attribute that provides security levels
login_manager.session_protection = 'strong'
# prefix denotes the location of the blueprint
login_manager.login_view = 'auth.login'

bootstrap = Bootstrap()  # creation of Bootstrap instance
db = SQLAlchemy()  # creation of a database instance
photos = UploadSet('photos', IMAGES)
mail = Mail()
simple = SimpleMDE()


def create_app(config_name):

    # creation of app instance with the __name__ variable
    app = Flask(__name__)

    # app configurations
    app.config.from_object(config_options[config_name])

    # initializing flask extensions
    # completing the initialization of bootstrap instance
    bootstrap.init_app(app)
    # calling the init_app method and passing in the application instance
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    simple.init_app(app)

    # registering main app Blueprint
    # import the instance that has been created
    from main import main as main_blueprint
    # calling the register_blueprint() method on the application instance and pass in the blueprint
    app.register_blueprint(main_blueprint)

    # registering authentication blueprint
    # registering the Blueprint instance.
    # from auth import auth as auth_blueprint
    # pass in url_prefix argument that will add a prefix to all the routes registered with that blueprint.
    # app.register_blueprint(auth_blueprint, url_prefix='/authenticate')

    # configure UploadSet
    # function which takes in the app and upload set instance
    configure_uploads(app, photos)

    return app
