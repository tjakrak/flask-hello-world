import sqlite3

import click
from flask import current_app, g


def get_db():
    
    # g is a special object that is unique for each request. 
    # It is used to store data that might be accessed by multiple functions during the request.
    if 'db' not in g:
        # sqlite3.connect() establishes a connection to the file pointed at by the DATABASE configuration key.
        g.db = sqlite3.connect(
            # current_app is another special object that points to the Flask application handling the request.
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )

        # sqlite3.Row tells the connection to return rows that behave like dicts. This allows accessing the columns by name.
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    # open_resource() opens a file relative to the flaskr package.
    # useful when deploying the application later since we won’t necessarily know where the location is
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# click.command() defines a command line command called init-db that calls the init_db function
@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db) # tells Flask to call that function when cleaning up after returning the response.
    app.cli.add_command(init_db_command) # adds a new command that can be called with the flask command.