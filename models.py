from werkzeug.security import generate_password_hash, check_password_hash
# implementation of methods (is_authenticated(), is_active(), is_anonymous(), get_id())
from flask_login import UserMixin
from . import login_manager, db


# modifies the load_user function by passing a user_id to the function that queries the database and gets a User with that ID
@login_manager.user_loader
def load_user(user_id):
    # call back function that retrieves a user when a unique identifier is passed
    return User.query.get(int(user_id))


# creation of a user class to help in creating new users. Pass in db.Model as argument for database connection and allow communication.
class User(UserMixin, db.Model):
    __tablename__ = 'users'  # allows us to give tables proper names.
    # integer will be stored as first argument
    id = db.Column(db.Integer, primary_key=True)
    # specifies strong column of 255 characters
    username = db.Column(db.String(255), unique=True, index=True)
    # enable users to have better access to their accounts
    email = db.Column(db.String(255), unique=True, index=True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))

    # creation of a virtual column that connects to the foreign key.
    pitches = db.relationship('Pitch', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')

    @property  # write only class property password. This generates a password has & pass the hashed password as a value to the pass_secure column property to save to the database
    def password(self):
        # Blocks access to the password property.
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        # generates has password and saves it to the pass_secure column property as a value.
        self.pass_secure = generate_password_hash(password)

    def verify_password(self, password):
        # takes in password, hashes it and compared it to hashed password to check similarity
        return check_password_hash(self.pass_secure, password)

    def __repr__(self):  # debugging mechanism
        return f'User {self.username}'


