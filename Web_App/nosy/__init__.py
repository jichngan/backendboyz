from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '08a42de617feebecee72fc928b3e4eb5'
app.config["CLIENT_IMAGES"] = "downloads/"
app.config["UPLOADED_POSTS_DEST"] = "nosy/static/uploads/"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['UPLOADED_PROFILE_PIC'] = "nosy/static/profile_pics/"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from nosy import routes