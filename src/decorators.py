from functools import wraps

from flask import session, redirect, url_for, request

from src.config import ADMINS


def requires_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for("user.login", next=request.path))
        return func(*args, **kwargs)
    return decorated_function


def requires_admin(func):
    @wraps(func)
    def is_admin(*args, **kwargs):
        if not session['email'] in ADMINS:
            return redirect(url_for("home_page", next=request.path))
        return func(*args, **kwargs)
    return is_admin
