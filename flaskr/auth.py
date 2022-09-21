import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

'''
@bp.route associates the URL /register with the register view function. 
When Flask receives a request to /auth/register, it will call the register view
and use the return value as the response.
'''
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

'''
When using a blueprint, the name of the blueprint is prepended to the name of the function, 
so the endpoint for the login function is 'auth.login' because we added it to the 'auth' blueprint.
'''
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone() # returns one row from the query

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id'] # session is a dict that stores data across requests
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

'''
bp.before_app_request() - registers a function that runs before the view function, 
no matter what URL is requested. 
'''
@bp.before_app_request
# This function checks if a user id is stored in the session 
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        # If there is no user id, or if the id doesn’t exist, g.user will be None
        g.user = None
    else:
        # gets user’s data from the database, storing it on g.user, which lasts for the length of the request
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

'''
This decorator returns a new view function that wraps the original view it is applied to.
The new function checks if a user is loaded and redirects to the login page otherwise. 
If a user is loaded the original view is called and continues normally.
'''
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            # The url_for() function - generates the URL to a view based on a name and arguments. 
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view