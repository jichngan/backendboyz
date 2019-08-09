from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = '08a42de617feebecee72fc928b3e4eb5'
app.config["CLIENT_IMAGES"] = "downloads/"
app.config["UPLOADED_POSTS_DEST"] = "nosy/static/uploads/"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['UPLOADED_PROFILE_PIC'] = "nosy/static/profile_pics/"
app.config['SOCIAL_FACEBOOK'] = {
    'consumer_key': '2080439705599157',
    'consumer_secret': 'e814fa92a9e377a052dcaafdbace4ea5'
}

app.config['SECURITY_POST_LOGIN'] = '/profile'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'boyzbackend@gmail.com'
app.config['MAIL_PASSWORD'] = 'B@ckendb0yz'
mail= Mail(app)


from nosy import routes