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

# Pitch class that will define tha different pitches and categories.


class Pitch(db.Model):
    __tablename__ = 'pitches'
    id = db.Column(db.Integer, primary_key=True)
    pitch_content = db.Column(db.String())
    pitch_category = db.Column(db.String(255))
    # stipulates that this is a foreign key and is the ID of a Users Model
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def save_pitch(self):
        """
        function that saves a pitch
        """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_pitch(cls, id):
        """
        function that gets a pitch by id
        """
        pitches = Pitch.query.filter_by(id=id).all()
        return pitches

    @classmethod
    def get_all_pitches(cls):
        """
        function that gets all the pitches
        """
        pitches = Pitch.query.order_by('-id').all()
        return pitches

    @classmethod
    def get_category(cls, cat):
        """
        function that gets category through search
        """
        category = Pitch.query.filter_by(
            pitch_category=cat).order_by('-id').all()
        return category

