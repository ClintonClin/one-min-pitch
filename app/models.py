from . import login_manager, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'  
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, index=True)
    email = db.Column(db.String(255), unique=True, index=True)
    bio = db.Column(db.String(255))
    pass_secure = db.Column(db.String(255))
    pitches = db.relationship('Pitch', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')

    @property  
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)

    def __repr__(self): 
        return f'User {self.username}'

class Pitch(db.Model):
    __tablename__ = 'pitches'
    id = db.Column(db.Integer, primary_key=True)
    pitch_content = db.Column(db.String())
    pitch_category = db.Column(db.String(255))
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


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment_content = db.Column(db.String())
    pitch_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, id):
        comments = Comment.query.filter_by(pitch_id=id).all()
        return comments
