"""
Primary Flask app

"""
import logging
import os
from flask import Flask, render_template, request,Response
from flask_cors import CORS
from app.api import api as api_blueprint
from app.errors import add_error_handlers
from app.config import Config
from flask_bcrypt import Bcrypt
from app.posts.processOCR import getData

from .extensions import (
    bcrypt,
    cache,
    csrf_protect,
    db,
    debug_toolbar,
    login_manager,
    migrate,
    mail,
)

from .models import *

logger = logging.getLogger()
def create_app(Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config["CACHE_TYPE"] = 'simple'
    CORS(app, resources={r'/*': {'origins': '*'}})
    
    register_extensions(app)
    from app.users.routes import users
    from app.posts.routes import posts
    from app.main.routes import main
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    add_error_handlers(app)
    # app.config['PUBSUB_VERIFICATION_TOKEN'] = \
    # os.environ['PUBSUB_VERIFICATION_TOKEN']
    # app.config['PUBSUB_TOPIC'] = os.environ['PUBSUB_TOPIC']
    # app.config['PROJECT'] = os.environ['GOOGLE_CLOUD_PROJECT']
    return app

def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    login_manager.login_view = 'users.login'
    login_manager.login_message_category = 'info'
    login_manager.init_app(app)
    migrate.init_app(app, db,compare_type=True)
    return None

application = create_app(Config)

@application.route('/admin/dbupgrade')
def dbupgrade():
    from flask_migrate import upgrade, Migrate
    migrate = Migrate(application, db)
    upgrade(directory=migrate.directory)
    return 'migrated'

@application.route('/temp/processdata')
def ocrData():
    return getData()

# @application.route('/admin/flask/')
# def create_tables():
# 	from flask_migrate import upgrade, Migrate
#     migrate = Migrate(application, db)
#     upgrade(directory=migrate.directory)
#     return 'migrated'
#https://networklore.com/start-task-with-flask/
'''
gcloud functions deploy Translate --runtime=python37 --entry-point=parse_message --trigger-topic=ocr --set-env-vars GOOGLE_CLOUD_PROJECT=gae-cloud-asu 
'''