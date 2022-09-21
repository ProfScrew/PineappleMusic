from unicodedata import name
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#from Codice.database import Session_artist

from models import *

from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

engine = create_engine('postgresql://artists:PassArtists@129.152.15.83:5432/PineappleMusic', echo=True)


Session = sessionmaker(bind=engine)       # factory pattern
session = Session()

#user = session.query(User.username,User.name,User.surname,User.birthdate,User.email,User.gender,User.phone,User.password,NormalListener.username.label('normallistener'),PremiumListener.username.label('premiumlistener'),Artist.username.label('artist')).outerjoin(NormalListener).outerjoin(PremiumListener).outerjoin(Artist).filter(User.username == 'JackSparrow').first()

#user = User.query.get('JackSparrow')

query = update(Song).where(Song.idsong == 23).values(name = 'Neila')
                
session.add(query)

session.commit()




#quer = select(NormalListener, User).join(NormalListener.username)

#a =  session.query(User).join(NormalListener)
#a = session.query(User).filter(User.username=='Matrix')
#print(a)



#for u, a in session.query(NormalListener).filter(User.id == Address.user_id):
#    print("({}, {})".format(u,a))


#session.delete(jack)


#our_user = session.query(User).filter_by(name='ed').first()    # qui è necessario salvare la pending instance
#our_user

#session.query(User).filter(User.username == 'JackSparrow').update({User.username: 'CaptainJackSparrow'})
#session.commit()

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