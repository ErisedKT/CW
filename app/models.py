from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db, login
from flask_login import UserMixin
from app import app
from time import time

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    image_file = db.Column(db.String(20))
    phone_number = db.Column(db.String(10), unique=True)
    aadhar = db.Column(db.String(10), unique=True)
    gender = db.Column(db.String(6), index=True)
    dob = db.Column(db.String(10))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %s>' % (self.first_name + self.last_name)      


@login.user_loader
def load_user(id):
    return User.query.get(int(id))