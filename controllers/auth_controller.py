from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from forms import LoginForm, RegisterForm
from services.auth_service import email_exists, register_user, authenticate_user

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = authenticate_user(form.email.data, form.password.data)
        if user:
            print(f"Login successful for user: {user.id}")
            login_user(user, remember=form.remember.data)
            print(f"User logged in: {current_user.is_authenticated}")
            return redirect(url_for('recipe.home'))
        flash('אימייל או סיסמה לא נכונים', 'error')
    return render_template('login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if email_exists(form.email.data):
            flash('האימייל הזה כבר רשום במערכת. אנא השתמש באימייל אחר.', 'error')
        else:
            user = register_user(form.username.data,
                                 form.email.data, form.password.data)
            print('user', user)
            if user:
                flash('נרשמת בהצלחה! כעת ניתן להתחבר')
                return redirect(url_for('auth.login'))
            flash('שגיאה בהרשמה. אנא נסה שנית.', 'error')
    return render_template('register.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('התנתקת בהצלחה')
    return redirect(url_for('recipe.home'))
