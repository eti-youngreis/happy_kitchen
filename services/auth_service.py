from werkzeug.security import check_password_hash, generate_password_hash
from models.models import User
from extensions import db

def email_exists(email):
    return User.query.filter_by(email=email).first() is not None

def register_user(username, email, password):
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def authenticate_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        return user
    return None

def get_user_by_id(user_id):
    return User.query.get(int(user_id))
