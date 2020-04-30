"""
Primary Flask app

"""
import logging
import os
from flask import Flask, render_template, request,Response
from flask_cors import CORS
from .api import api as api_blueprint
from .errors import add_error_handlers
from .config import ConfigProd as Config
from flask_bcrypt import Bcrypt
from .extensions import (
    db,
    migrate,
    bcrypt,
)
from .models import *

logger = logging.getLogger()
def create_app(Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    CORS(app, resources={r'/*': {'origins': '*'}})
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')
    register_extensions(app)
    add_error_handlers(app)
    return app

def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    db.init_app(app)

    migrate.init_app(app, db,compare_type=True)
    return None

application = create_app(Config)

@application.route('/admin/dbupgrade')
def dbupgrade():
    from flask_migrate import upgrade, Migrate
    migrate = Migrate(application, db)
    upgrade(directory=migrate.directory)
    return 'migrated'




# @application.route('/admin/flask/')
# def create_tables():
# 	from flask_migrate import upgrade, Migrate
#     migrate = Migrate(application, db)
#     upgrade(directory=migrate.directory)
#     return 'migrated'

