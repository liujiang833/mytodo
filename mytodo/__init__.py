import os
from flask import Flask
import datetime


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # PERMANENT_SESSION_LIFETIME=datetime.timedelta(minutes=1)
    )

    app.static_folder = 'static'
    # if test_config is None:
    #     # load the instance config, if it exists, when not testing
    #     app.config.from_pyfile('config.py', silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Welcome!'

    # all blueprints
    from . import auth
    app.register_blueprint(auth.bp)

    from . import mytodo
    app.register_blueprint(mytodo.bp)
    app.add_url_rule('/', endpoint='index')
    return app
