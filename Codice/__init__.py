import imp
from flask import Flask
from flask_login import LoginManager

from Codice.config import config
from Codice.models import User
from Codice.database import *

#problema inclusione circolare
from .auth.routes import auth
from .user.routes import user
from .error.routes import error
from .artist.routes import artist
from .music.routes import music

# initializing the webapp
app = Flask(__name__)

# setting secret key
app.config['SECRET_KEY'] = config['SECRET_KEY']

# settig flask-sqalchemy database connection
app.config['SQLALCHEMY_DATABASE_URI'] = config['GUEST_MANAGER_DB']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



# setting up native flask-login manager
login_manager = LoginManager()
login_manager.login_view = 'auth.signin'


@login_manager.user_loader
# user loader
def load_user(user_id):
    return User.query.get(user_id)


login_manager.init_app(app)

# setting flask max dimensions of uploaded files to prevent crash and errors
app.config['MAX_CONTENT_PATH'] = 10485760

app.config['UPLOAD_FOLDER'] = "/tmp/"

with app.app_context():
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(error, url_prefix='/error')
    app.register_blueprint(artist, url_prefix='/artist')
    app.register_blueprint(music, url_prefix='/music')


    
    
