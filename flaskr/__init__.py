import os

from flask import Flask

# all the local packages
from . import db
from . import auth
from . import blog

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # # a simple page that says hello
    # @app.route('/hello')
    # def hello():
    #     return 'Hello, World!'

    # intialize db
    db.init_app(app)

    # import and register the auth blueprint from the factory
    app.register_blueprint(auth.bp)

    # import and register the blog blueprint from the factory
    app.register_blueprint(blog.bp)
    # app.add_url_rule() - associates the endpoint name 'index' with the / url
    # so that url_for('index') or url_for('blog.index') will both work
    app.add_url_rule('/', endpoint='index')

    return app