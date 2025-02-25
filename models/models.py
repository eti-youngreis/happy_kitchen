from datetime import datetime, timezone

from flask_login import UserMixin
from extensions import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(80), unique=True, nullable=False)
    email = db.Column(db.Unicode(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.now(timezone.utc))
    recipes = db.relationship('Recipe', backref='author', lazy=True)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(100), nullable=False)
    ingredients = db.Column(db.UnicodeText, nullable=False)
    instructions = db.Column(db.UnicodeText, nullable=False)
    created_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.now(timezone.utc))
    difficulty = db.Column(db.Unicode(20), nullable=False)
    course_type = db.Column(db.Unicode(20), nullable=False)
    dairy_type = db.Column(db.Unicode(20), nullable=False)
    image_path = db.Column(db.Unicode(255), nullable=False)
    cooking_time = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
