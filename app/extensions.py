# # from flask_bcrypt import Bcrypt
# # from flask_login import LoginManager
# from flask_migrate import Migrate
# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt

# bcrypt = Bcrypt()
# # csrf_protect = CSRFProtect()
# # login_manager = LoginManager()
# db = SQLAlchemy()
# migrate = Migrate()
# # cache = Cache()
# # debug_toolbar = DebugToolbarExtension()
# # mail = Mail()

from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_webpack import Webpack
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail

bcrypt = Bcrypt()
csrf_protect = CSRFProtect()
login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
cache = Cache()
debug_toolbar = DebugToolbarExtension()
mail = Mail()