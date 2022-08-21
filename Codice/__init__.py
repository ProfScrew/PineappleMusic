from flask import Flask
from requests import Session

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session

from flask_login import LoginManager

from Codice.config import config





# initializing the webapp
app = Flask(__name__)

# setting secret key
app.config['SECRET_KEY'] = config['SECRET_KEY']

# settig flask-sqalchemy database connection
app.config['SQLALCHEMY_DATABASE_URI'] = config['GUEST_MANAGER_DB']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# setting sqlalchemy connection
engine_artist = create_engine(config['ARTIST_DB'], echo=True)
engine_listener = create_engine(config['LISTENER_DB'], echo=True)
engine_premiumlistener = create_engine(config['PREMIUMLISTENER_DB'], echo=True)
engine_guestmanager = create_engine(config['GUEST_MANAGER_DB'], echo=True)

# genero le sessioni per ogni ruolo
Session = scoped_session(sessionmaker(bind=engine_artist))
Session_artist = Session()
Session = scoped_session(sessionmaker(bind=engine_listener))
Session_listener = Session()
Session = scoped_session(sessionmaker(bind=engine_premiumlistener))
Session_premiumlistener = Session()
Session = scoped_session(sessionmaker(bind=engine_guestmanager))
Session_guestmanager = Session()

Base = declarative_base()
Base.query = Session.query_property()

# setting up native flask-login manager
login_manager = LoginManager()
login_manager.login_view = 'auth.signin'

from Codice.models import User

@login_manager.user_loader
# user loader
def load_user(user_id):
    return User.query.get(user_id)


login_manager.init_app(app)

# setting flask max dimensions of uploaded files to prevent crash and errors
app.config['MAX_CONTENT_PATH'] = 10485760

app.config['UPLOAD_FOLDER'] = "/tmp/"

with app.app_context():
    from .home.routes import home
    from .auth.routes import auth
    
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(home, url_prefix='/home')


    
    
