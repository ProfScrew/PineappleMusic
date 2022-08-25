import sqlalchemy
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from models import *


engine = create_engine('postgresql://premium_listeners:PassPremiumListeners@129.152.15.83:5432/PineappleMusic', echo=True)


Session = sessionmaker(bind=engine)       # factory pattern
session = Session()

for instance in session.query(User):
    print(instance)

premiumlistener = PremiumListener('Matrix')
session.add(premiumlistener)
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