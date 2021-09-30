import calendar
import json

from .auth import login, login_required
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from datetime import date, time
from .util import str_to_date, str_to_time
from .database import dbdriver

bp = Blueprint('mytodo', __name__)

NOT_READY = "Not ready"

default_time = time()


@bp.route('/')
@login_required
def index():
    # g.month_info = get_todos_month_default()
    return render_template("month.html")


@bp.context_processor
def current_date_processor():
    def get_current_date():
        return date.today().strftime("%B, %Y")

    return dict(get_current_date=get_current_date)


@bp.route('/content/range', methods=['POST'])
def content():
    start_date = str_to_date(request.form['start_date'])
    end_date = str_to_date(request.form['end_date'])
    if start_date is None or end_date is None or session.get('token') is None:
        return json.dumps([])
    return dbdriver.get_todos_json(session['token'], start_date, end_date)


@bp.route('/content/month', methods=['POST'])
def content_month():
    curr_date = str_to_date(request.form['date'])
    if curr_date is None or session.get('token') is None:
        return json.dumps([])
    month_dates = list(calendar.Calendar().itermonthdates(curr_date.year, curr_date.month))
    start_date, end_date = month_dates[0], month_dates[-1]
    return dbdriver.get_todos_json(session['token'], start_date, end_date)


@bp.route('/content/add_todo', methods=['POST'])
def add_todo():
    todo_date = str_to_date(request.form['date'])
    title = request.form['title']
    description = request.form['description']
    start_time = str_to_time(request.form['start_time']) if request.form.get('start_time') is not None else default_time
    end_time = str_to_time(request.form['end_time']) if request.form.get('end_time') is not None else default_time
    if todo_date is None or start_time is None or end_time is None \
            or session.get('token') is None or session.get('user_id') is None:
        return "Fail"

    dbdriver.add_todo(session['user_id'], title, description, todo_date, start_time, end_time)
    return dbdriver.get_todos_json(session['token'], todo_date, todo_date)


@bp.route('/content/update_todo', methods=['POST'])
def update_todo():
    todo_date = str_to_date(request.form['date'])
    title = request.form['title']
    description = request.form['description']
    start_time = str_to_time(request.form['start_time']) if request.form.get('start_time') is not None else default_time
    end_time = str_to_time(request.form['end_time']) if request.form.get('end_time') is not None else default_time
    todo_number = request.form.get('todo_number')
    if todo_date is None or start_time is None or end_time is None \
            or session.get('token') is None or session.get('user_id') is None \
            or todo_number is None:
        return "Fail"

    if not dbdriver.update_todo(session['user_id'], title, description, todo_date, start_time, end_time, todo_number):
        return "Fail"
    return dbdriver.get_todos_json(session['token'], todo_date, todo_date)


@bp.route('/content/delete_todo', methods=['POST'])
def delete_todo():
    todo_number = request.form.get('todo_number')
    if session.get('token') is None or session.get('user_id') is None \
            or todo_number is None:
        return "Fail"
    todo_date = dbdriver.delete_todo(todo_number)
    if todo_date is None:
        return "Fail"

    return dbdriver.get_todos_json(session['token'], todo_date, todo_date)
