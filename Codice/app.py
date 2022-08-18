import sqlalchemy
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from models import *


engine = create_engine('postgresql://guest_manager:PassGuestManager@localhost:5432/PinappleMusic', echo=True)


Session = sessionmaker(bind=engine)       # factory pattern
session = Session()

for instance in session.query(User):
    print(instance)


#session.query(User).filter(User.username == 'JackSparrow').update({User.username: 'CaptainJackSparrow'})
#session.commit()
