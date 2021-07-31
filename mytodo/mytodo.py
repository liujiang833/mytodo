from .auth import login, login_required
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from datetime import date

bp = Blueprint('mytodo', __name__)

NOT_READY = "Not ready"


@bp.route('/')
@login_required
def index():
    # g.month_info = get_todos_month_default()
    return render_template("day.html")


@bp.context_processor
def current_date_processor():
    def get_current_date():
        return date.today().strftime("%B, %Y")

    return dict(get_current_date=get_current_date)


@bp.route('/content', methods=['POST'])
def content():
    pass
