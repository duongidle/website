from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class ResetPasswordRequestForm(FlaskForm):
    email = StringField(('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField()

class ResetPasswordForm(FlaskForm):
    password = PasswordField(('Nhập mật khẩu mới'), validators=[DataRequired()])
    password2 = PasswordField(
        ('Nhập lại mật khẩu mới'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(('SUBMIT'))

