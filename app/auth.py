from flask import Blueprint, render_template, request, flash, redirect, url_for, Flask
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        details = request.form
        email = details['inputEmail']
        password = details['inputPassword']

        user = User.query.filter_by(user_email=email).first()
        if user:
            if check_password_hash(user.user_password, password):
                flash('Dang nhap thanh cong!', category='success')
                return render_template('index.html', user=current_user)
            else:
                flash('Mat khau khong dung!', category='error')
        else:
            flash('Nguoi dung khong ton tai!', category='error')
            
    return render_template('signin.html', user=current_user)

@auth.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        details = request.form
        name = details['inputName']
        email = details['inputEmail']
        password1 = details['inputPassword']
        password2 = details['inputRepeatPassword']
        phoneNumber = details['inputPhoneNumber']
        
        user = User.query.filter_by(user_email=email).first()
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
            new_user = User(user_email=email, user_name=name, user_password=generate_password_hash(password1, method='sha256'), phone_number = phoneNumber)
            db.session.add(new_user)
            db.session.commit()
            flash('Tai khoan da duoc tao, vui long dang nhap lai!', category='success')
            return render_template('signin.html')
    return render_template('signup.html', user=current_user)
