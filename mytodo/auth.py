from flask import Blueprint, flash, g, redirect, render_template, request, url_for
import string
import random
import functools

from flask.globals import session
from .database import DbDriver

dbdriver = DbDriver()
dbdriver.connect_to_db()
bp = Blueprint('auth', __name__, url_prefix='/auth')

NOT_READY = "Not ready yet"


@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        token = dbdriver.get_user(request.form['token'])
        if token is None:
            flash('invalid token')
        else:
            session.clear()
            session['token'] = token
            return redirect(url_for('index'))

    return render_template('auth/login.html')


@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        token = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(32))
        # print('token')
        dbdriver.add_user(token)
        return token
    return render_template('auth/register.html')


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


@bp.before_app_request
def load_logged_in_user():
    g.user_id = session.get('user_id')


def login_required(view):

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get('token') is None:
            flash("Login required!\n")
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view
