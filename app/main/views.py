from flask import render_template, request, redirect, url_for, flash, abort
from . import main
from ..models import User, Pitch, Comment
from flask_login import login_required, current_user
from .. import db, photos
from .forms import PitchForm, CommentForm, UpdateProfile
import markdown2


@main.route('/')
def index():
    '''
    root page function that returns the index page and its data
    '''
    title = "Welcome to PitchBlack"

    return render_template("index.html", title=title)


@main.route('/user/<uname>&<id_user>')
@login_required
def profile(uname, id_user):
    user = User.query.filter_by(username=uname).first()

    title = f"{uname.capitalize()}'s Profile"

    get_pitches = Pitch.query.filter_by(user_id=id_user).all()
    get_comments = Comment.query.filter_by(user_id=id_user).all()

    if user is None:
        abort(404)

    return render_template('profile/profile.html', user=user, title=title, pitches_no=get_pitches,
                           comments_no=get_comments)


@main.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    pitch_form = PitchForm()

    if pitch_form.validate_on_submit():
        pitch = pitch_form.pitch.data
        cat = pitch_form.my_category.data

        new_pitch = Pitch(pitch_content=pitch,
                          pitch_category=cat, user=current_user)
        new_pitch.save_pitch()

        return redirect(url_for('main.home'))

    all_pitches = Pitch.get_all_pitches()

    title = 'Home'
    return render_template('home.html', title=title, pitch_form=pitch_form, pitches=all_pitches)


@main.route('/pitch/<int:id>', methods=['GET', 'POST'])
@login_required
def pitch(id):
    my_pitch = Pitch.query.get(id)
    comment_form = CommentForm()

    if id is None:
        abort(404)

    if comment_form.validate_on_submit():
        comment_data = comment_form.comment.data
        new_comment = Comment(comment_content=comment_data,
                              pitch_id=id, user=current_user)
        new_comment.save_comment()

        return redirect(url_for('main.pitch', id=id))

    all_comments = Comment.get_comments(id)

    title = 'Comment'
    return render_template('pitch.html', pitch=my_pitch, comment_form=comment_form, comments=all_comments, title=title)


@main.route('/category/<cat>')
def category(cat):
    my_category = Pitch.get_category(cat)

    title = f'{cat} category | One Minute Pitch'

    return render_template('category.html', title=title, category=my_category)


@main.route('/user/<uname>/update', methods=['GET', 'POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()

    if user is None:
        abort(404)

    update_form = UpdateProfile()

    if update_form.validate_on_submit():
        user.bio = update_form.bio.data
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', uname=user.username, id_user=user.id))
    title = 'Update Bio'
    return render_template('profile/update.html', form=update_form, title=title)


@main.route('/user/<uname>/update/pic', methods=['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username=uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile', uname=uname, id_user=current_user.id))
