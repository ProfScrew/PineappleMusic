from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from requests import Session

from Codice.fastconfig import config
from Codice.models import create_engine

# setting sqlalchemy connection
engine_artist = create_engine(config['ARTIST_DB'], echo=True, isolation_level="AUTOCOMMIT")
engine_listener = create_engine(config['LISTENER_DB'], echo=True, isolation_level="AUTOCOMMIT")
engine_premiumlistener = create_engine(config['PREMIUMLISTENER_DB'], echo=True, isolation_level="AUTOCOMMIT")
engine_guestmanager = create_engine(config['GUEST_MANAGER_DB'], echo=True, isolation_level="AUTOCOMMIT")
engine_deletemanager = create_engine(config['DELETE_MANAGER_DB'], echo=True, isolation_level="AUTOCOMMIT")

# genero le sessioni per ogni ruolo
Session = scoped_session(sessionmaker(bind=engine_artist))
Session_artist = Session()
Session = scoped_session(sessionmaker(bind=engine_listener))
Session_listener = Session()
Session = scoped_session(sessionmaker(bind=engine_premiumlistener))
Session_premiumlistener = Session()
Session = scoped_session(sessionmaker(bind=engine_deletemanager))
Session_deletemanager = Session()
Session = scoped_session(sessionmaker(bind=engine_guestmanager))
Session_guestmanager = Session()