from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.main.forms import EditProfileForm
from app.models import User
from app.main import bp


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/review', methods=['GET', 'POST'])
def review():
    return render_template('review/review.html')

@bp.route('/homepage', methods=['GET', 'POST'])
@login_required
def homepage():
    return render_template('home.html')

@bp.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('review/about.html')

@bp.route('/term', methods=['GET', 'POST'])
def term():
    return render_template('review/term.html')

@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@bp.route('/tool/<username>')
@login_required
def tool(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('application.html', user=user)

