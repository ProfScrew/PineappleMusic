
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.sql.functions import count
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

#from Codice.database import Session_artist

from models import *

from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

engine = create_engine('postgresql://artists:PassArtists@localhost:5432/PineappleMusic', echo=True)



Session = sessionmaker(bind=engine)       # factory pattern
session = Session()



count_of_genre = session.query(Genre.name.label("genre"),
                             count(Record.song).label("likes")).join(Belong).join(Song).join(Record).filter(and_(Record.vote == True,
                                                                                                                 Record.user == 'JackSparrow')).order_by(desc("likes")).group_by(Genre.name).all()
total_likes = 0
for i in count_of_genre:
    total_likes = total_likes + i.likes
arr = []
for i in count_of_genre:
    temp = round(((i.likes * 100) / total_likes)/10)
    if temp != 0:
        col = []
        col.append(i.genre)
        col.append(temp)
        arr.append(col)
        
songs = []
for i in arr:
    print("Genre: ", i[0])
    #song = sqlalchemy.sql.select(Song).join(Belong).filter(Belong.genre == i[0]).limit(i[1])
    song = session.query(Song.name.label("name"),
                                           Song.cover.label("cover"),
                                           Belong.genre.label("genre"),
                                           Creates.username.label("artist"),
                                           Album.name.label("album"),
                                           Statistic.views.label("views")).join(Belong).join(Creates).outerjoin(Album).join(Statistic).order_by(desc(Statistic.views)).filter(Belong.genre == i[0]).limit(i[1])
    if i == arr[0]:
        result_query = song
    else:
        result_query = union(result_query, song)
    for j in songs:
        print(j)
result = session.execute(result_query).all()
    


#result = songs[0].union(songs[1],songs[2]).all()

print("Result:--------------------------")
for i in result:
    
    print(i)
print("All:------------------------")
print(result)
    
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