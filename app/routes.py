from flask import render_template, url_for, flash, redirect, get_flashed_messages, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, DetailsForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from datetime import datetime
from PIL import Image
import os

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='Home')   

@login_required
@app.route('/explore')
def explore():
    users = User.query.all()
    return render_template('explore.html', title='Explore', users=users)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@login_required
@app.route('/details', methods=['GET', 'POST'])
def details():
    form = DetailsForm()
    if form.validate_on_submit():
        current_user.phone_number = form.phone.data
        current_user.aadhar = form.aadhar.data
        current_user.gender = form.gender.data
        save_picture(form.picture.data)
        current_user.image_file = form.picture.data.filename
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('explore'))
    return render_template('details.html', title='Add Details', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data,
                    dob=form.dob.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('details'))
    return render_template('register.html', title='Register', form=form)

def save_picture(form_picture):
    picture_path = os.path.join(app.root_path, 'static/profile_pics', form_picture.filename)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

@app.route('/user/<id>')
@login_required
def user(id):
    user = User.query.get(int(id))
    return render_template('user.html', user=user)
