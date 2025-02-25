from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    email = EmailField('אימייל', validators=[DataRequired(), Email()])
    password = PasswordField('סיסמה', validators=[DataRequired()])
    remember = BooleanField('זכור אותי')
    submit = SubmitField('התחבר')


class RegisterForm(FlaskForm):
    username = StringField('שם משתמש', validators=[
                           DataRequired(), Length(min=2, max=80)])
    email = EmailField('אימייל', validators=[DataRequired(), Email()])
    password = PasswordField('סיסמה', validators=[
        DataRequired(),
        Length(min=6, message='הסיסמה חייבת להכיל לפחות 6 תווים')
    ])
    submit = SubmitField('הרשמה')


class RecipeForm(FlaskForm):
    name = StringField('שם המתכון', validators=[DataRequired(), Length(min=2)])
    ingredients = TextAreaField('מצרכים', validators=[DataRequired()])
    instructions = TextAreaField('הוראות הכנה', validators=[DataRequired()])
    cooking_time = StringField('זמן הכנה', validators=[DataRequired()])
    difficulty = SelectField('רמת קושי', choices=['קל', 'בינוני', 'מורכב'])
    course_type = SelectField(
        'סוג מנה', choices=['מנה ראשונה', 'מנה עיקרית', 'קינוח'])
    dairy_type = SelectField('סוג חלבי', choices=['חלבי', 'בשרי', 'פרווה'])
    submit = SubmitField('העלה מתכון')
