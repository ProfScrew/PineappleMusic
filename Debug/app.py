
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.sql.functions import count
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

#from Codice.database import Session_artist

from ..Codice.models import Song, Artist, User, Creates, Session_guestmanager

from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

engine = create_engine('postgresql://artists:PassArtists@localhost:5432/PineappleMusic', echo=True)



Session = sessionmaker(bind=engine)       # factory pattern
session = Session()



for i in range(1, 8000):
    song = Song.get_songs('JackSparrow', session)
    for a in song:
        print(a)

    
#user = session.query(User.username,User.name,User.surname,User.birthdate,User.email,User.gender,User.phone,User.password,NormalListener.username.label('normallistener'),PremiumListener.username.label('premiumlistener'),Artist.username.label('artist')).outerjoin(NormalListener).outerjoin(PremiumListener).outerjoin(Artist).filter(User.username == 'JackSparrow').first()

#user = User.query.get('JackSparrow')


#songs = session.query(Song,Belong.genre,Creates.username,Album.name,Record).join(Belong).join(Creates).outerjoin(Album).outerjoin(Record).all()
#songs = session.query(Song).all()
#for i in songs:
#    print(i)



#record = session.query(Record).filter(Record.user == 'JackSparrow').subquery()
#songs = Song.query.outerjoin(record)
#print("AAAAAAAAAAAAAA ",songs)

#song = session.query(Song,Record).outerjoin(Record).all()
#record = session.query(Song, Record).outerjoin(Record).filter(Record.user == 'JackSparrow').all()
#query = song.union(record)


#songsjack = session.query(Record).filter(Record.user == 'JackSparrow').subquery()

    
#query = session.query(songsjack,Song).outerjoin(songsjack).limit(3).all()






#   last_orders = db.session.query(
#       Order.customer_id, db.func.max(Order.order_date).label('last_order_date')
#   ).group_by(Order.customer_id).subquery()
#   query = Order.query.join(
#       last_orders, Order.customer_id == last_orders.c.customer_id
#   ).order_by(last_orders.c.last_order_date.desc(), Order.order_date.desc())


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