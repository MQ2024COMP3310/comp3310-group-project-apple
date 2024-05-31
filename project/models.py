from datetime import datetime, timedelta
from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):  
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)  
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(200), nullable=False)  # (secure coding principles) Password is stored in hashed format
    is_admin = db.Column(db.Boolean, default=False)  # (secure coding principles) Admin flag to distinguish regular users from admin users
    failed_attempts = db.Column(db.Integer, default=0)  # (secure coding principles) Track failed login attempts
    is_locked = db.Column(db.Boolean, default=False)  # (secure coding principles) Lock the account after 5 failed attempts
    locked_until = db.Column(db.DateTime, nullable=True)  # (secure coding principles) Lock the account until a specific time

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    caption = db.Column(db.String(250), nullable=False)
    file = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(600), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Add user_id field

    @property
    def serialize(self):
       return {
           'id': self.id,
           'name': self.name,
           'caption': self.caption,
           'file': self.file,
           'desc': self.description,
       }