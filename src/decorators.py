from functools import wraps

from flask import session, redirect, url_for, request


def requires_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for("user.login", next=request.path))
        return func(*args, **kwargs)
    return decorated_function

