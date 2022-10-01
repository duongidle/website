from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
from flask_babel import _
from app import db
from app.auth import bp
from app.auth.forms import ResetPasswordRequestForm, ResetPasswordForm
from app.models import User
from app.auth.email import send_password_reset_email


@bp.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == "POST":
        details = request.form
        email = details['Email']
        password = details['Password']

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password_hash, password):
                return render_template('index.html', user=current_user)
            else:
                flash('Mat khau khong dung!', category='error')
        else:
            flash('Nguoi dung khong ton tai!', category='error')
            
    return render_template('auth/login.html', user=current_user)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == "POST":
        details = request.form
        name = details['inputName']
        email = details['inputEmail']
        password1 = details['inputPassword']
        password2 = details['inputRepeatPassword']
        phoneNumber = details['inputPhoneNumber']
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email da ton tai.', category='error')
        elif len(email) < 4:
            flash('Email khong chinh xac.', category='error')
        elif len(name) < 2:
            flash('Ten khong chinh xac.', category='error')
        elif password1 != password2:
            flash('Mat khau khong trung khop.', category='error')
        elif len(password1) < 7:
            flash('Mat khau khong hop le.', category='error')
        elif len(phoneNumber) < 9:
            flash('So dien thoai khong hop le.', category='error')
        else:
            new_user = User(email=email, username=name, password_hash=generate_password_hash(password1, method='sha256'), phone_number = phoneNumber)
            db.session.add(new_user)
            db.session.commit()
            flash('Tai khoan da duoc tao, vui long dang nhap lai!', category='success')
            return render_template('auth/login.html')
    return render_template('auth/register.html', user=current_user)


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(
            _('Check your email for the instructions to reset your password'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title=_('Reset Password'), form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)

