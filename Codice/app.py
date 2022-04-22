import sqlalchemy
from sqlalchemy import *

# SQLite supporta database transienti in RAM (echo attiva il logging)
engine = create_engine('postgresql://admin:ciao@localhost:5432/music', echo = True)
metadata = MetaData()

users = Table('song', metadata, Column('title', String),
                                 Column('IDsong', Integer, primary_key=True))


metadata.create_all(engine)       # nota: non sovrascrive le tabelle esistenti :)
conn = engine.connect()
s = select([users])
result = conn.execute(s)

type(result)

for row in result:
    print (row)