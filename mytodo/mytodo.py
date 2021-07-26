from mytodo.auth import NOT_READY
from .auth import login, login_required
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from datetime import date
from .database import get_todos_month, get_todos_month_default, get_todos_month_mock
bp = Blueprint('mytodo', __name__)

NOT_READY = "Not ready"

@bp.route('/')
# @login_required
def index():
    g.month_info = get_todos_month_default()
    print(g.month_info)
    return render_template("main_view.html")

@bp.context_processor
def current_date_processor():
    def get_current_date():
        return date.today().strftime("%B, %Y")
    return dict(get_current_date=get_current_date)
