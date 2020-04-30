# from flask_bcrypt import Bcrypt
# from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
# csrf_protect = CSRFProtect()
# login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
# cache = Cache()
# debug_toolbar = DebugToolbarExtension()
# mail = Mail()