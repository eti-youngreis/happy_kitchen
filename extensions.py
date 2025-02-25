from flask import flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    print(f'load_user: {user_id}')
    from services.auth_service import get_user_by_id
    return get_user_by_id(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    print("Unauthorized access attempted")
    flash('עליך להתחבר כדי לגשת לעמוד זה.', 'info')
    return redirect(url_for('auth.login'))
