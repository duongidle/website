from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from guess_language import guess_language
from app import db
from app.main.forms import EditProfileForm
from app.models import User
from app.translate import translate
from app.main import bp


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/review', methods=['GET', 'POST'])
def review():
    return render_template('review/review.html')

@bp.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('review/about.html')

@bp.route('/term', methods=['GET', 'POST'])
def term():
    return render_template('review/term.html')

@bp.route('/homepage', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html', title=_('Home'))

@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')


