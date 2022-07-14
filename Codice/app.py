
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



engine = create_engine('postgresql://guest_manager:PassGuestManager@localhost:5432/PinappleMusic', echo=True)

Base = declarative_base()                      # tabella = classe che eredita da Base

class User(Base):
    __tablename__ = 'users'                   # obbligatorio

    username = Column(String, primary_key=True)    # almeno un attributo deve fare parte della primary key
    name=Column(String)
    surname = Column(String)
    birthdate = Column(Date)
    password =Column(String)
    gender =Column(String)
    phone=Column(Integer)
    email=Column(String)
    
    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<User(username='%s', name='%s', surname='%s',birthdate='%s' password='%s', gender='%s',phone='%d',email='%s')>" % (self.username,self.name, self.surname, self.birthdate,self.password,self.gender,self.phone,self.email)


Session = sessionmaker(bind=engine)       # factory pattern
session = Session()

for instance in session.query(User):
    print(instance)


session.query(User).filter(User.username == 'JackSparrow').update({User.username: 'CaptainJackSparrow'})
session.commit()

'''
from datetime import date
import string
import sqlalchemy as db
# from sqlalchemy import *

# SQLite supporta database transienti in RAM (echo attiva il logging)
engine = db.create_engine('postgresql://listeners:PassListeners@localhost:5432/PinappleMusic', echo = True)
#connection = engine.connect()
metadata = MetaData()
Session = ses

#users = db.Table('users', metadata, autoload=True, autoload_with=engine)
users = db.Table('users', metadata, Column('username', String, primary_key=True),
                                 Column('name', String),
                                 Column('surname', String),
                                 Column('birthdate', Date),
                                 Column('password', String),
                                 Column('gender', String),
                                 Column('phone', Integer),
                                 Column('email', String)
                                 )


query = db.select([users])

resultP = connection.execute(query)

resultS = resultP.fetchall()
print(resultS)

'''


# metadata.create_all(engine)       # nota: non sovrascrive le tabelle esistenti :)

# conn = engine.connect()
# s = select([users])
# result = conn.execute(s)

# print(type(users.username))

# type(result)

# for row in result:
#     print (row)