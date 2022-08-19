from flask import Flask
from requests import Session

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import *

from flask_login import LoginManager

from Codice.config import config
from Codice.models import User


def create_app():

    # initializing the webapp
    app = Flask(__name__)

    # setting up native flask-login manager
    #login_manager = LoginManager()
    # login_manager.init_app(app)

    # setting secret key
    app.config['SECRET_KEY'] = config['SECRET_KEY']

    # settig flask-sqalchemy database connection
    app.config['SQLALCHEMY_DATABASE_URI'] = config['GUEST_MANAGER_DB']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # setting sqlalchemy connection
    engine_artist = create_engine(config['ARTIST_DB'], echo=True)
    engine_listener = create_engine(config['LISTENER_DB'], echo=True)
    engine_premiumlistener = create_engine(
        config['PREMIUMLISTENER_DB'], echo=True)
    engine_guestmanager = create_engine(config['GUEST_MANAGER_DB'], echo=True)

    # genero le sessioni per ogni ruolo
    Session = sessionmaker(bind=engine_artist)
    Session_artist = Session()
    Session = sessionmaker(bind=engine_listener)
    Session_listener = Session()
    Session = sessionmaker(bind=engine_premiumlistener)
    Session_premiumlistener = Session()
    Session = sessionmaker(bind=engine_guestmanager)
    Session_guestmanager = Session()

    # setting flask max dimensions of uploaded files to prevent crash and errors
    app.config['MAX_CONTENT_PATH'] = 10485760

    # setting upload folder
    app.config['UPLOAD_FOLDER'] = "/tmp/"

    with app.app_context():

        from .auth import routes

        app.register_blueprint(routes.auth, url_prefix='/auth')

        return app
