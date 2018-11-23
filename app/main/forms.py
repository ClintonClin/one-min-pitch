from flask_wtf import FlaskForm  # Class to help us create a form class
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import Required


class PitchForm(FlaskForm):  # inherits from the FlaskForm
    title = StringField('Pitch title', validators=[Required()])
    pitch = TextAreaField('Your Pitch', validators=[Required()])
    my_category = SelectField('Category', choices=[('Technology', 'Technology'), ('Fiction', 'Fiction'), ('Automotive', 'Automotive')], validators=[Required()])
    submit = SubmitField('Live your life to the fullest!')


class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[Required()])
    submit = SubmitField('Post Comment')


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us more about you.', validators=[Required()])
    submit = SubmitField('Submit')
