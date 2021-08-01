from datetime import date, time


def str_to_date(date_str: str):
    try:
        date_obj = date.fromisoformat(date_str)
    except ValueError:
        date_obj = None
    return date_obj


def str_to_time(time_str: str):
    try:
        time_obj = time.fromisoformat(time_str)
    except ValueError:
        time_obj = None
    return time_obj
