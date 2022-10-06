from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user
from flask_babel import _
from app import db
from app.auth import bp
from app.auth.forms import ResetPasswordRequestForm, ResetPasswordForm
from app.models import User
from app.auth.email import send_password_reset_email

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))

    if request.method == "POST":
        details = request.form
        email = details['Email']
        password = details['Password']

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password_hash, password):
                login_user(user)
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('main.homepage')
                return redirect(next_page)
            else:
                flash('Mật khẩu không đúng!', category='error')
        else:
            flash('Người dùng không tồn tại.', category='error')
            
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.review'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))

    if request.method == "POST":
        details = request.form
        name = details['inputName']
        email = details['inputEmail']
        password1 = details['inputPassword']
        password2 = details['inputRepeatPassword']
        phoneNumber = details['inputPhoneNumber']
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email đã tồn tại.', category='error')
        elif len(email) < 4:
            flash('Email không chính xác.', category='error')
        elif len(name) < 2:
            flash('Tên không chính xác.', category='error')
        elif password1 != password2:
            flash('Mật khẩu không trùng khớp.', category='error')
        elif len(password1) < 7:
            flash('Mật khẩu không hợp lệ.', category='error')
        elif len(phoneNumber) < 9:
            flash('Số điện thoại không hợp lệ.', category='error')
        else:
            new_user = User(email=email, username=name, password_hash=generate_password_hash(password1, method='sha256'), phone_number = phoneNumber)
            db.session.add(new_user)
            db.session.commit()
            flash('Tài khoản đã được tạo, vui lòng đăng nhập lại!', category='success')
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html', user=current_user)


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Vui lòng kiểm tra email. Nếu không nhận được phản hồi sau 10 phút, vui lòng liên hệ quản trị!')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/reset_password_request.html', form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.homepage'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Mật khẩu của bạn đã được khôi phục.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)

