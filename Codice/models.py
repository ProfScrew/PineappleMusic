import sqlalchemy
from sqlalchemy import *

# USERS


class User():
    __tablename__ = 'users'                   # obbligatorio

    # almeno un attributo deve fare parte della primary key
    username = Column(String, primary_key=True)
    name = Column(String)
    surname = Column(String)
    birthdate = Column(Date)
    password = Column(String)
    gender = Column(String)
    phone = Column(Integer)
    email = Column(String)

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<User(username='%s', name='%s', surname='%s',birthdate='%s' password='%s', gender='%s',phone='%d',email='%s')>" % (self.username, self.name, self.surname, self.birthdate, self.password, self.gender, self.phone, self.email)


class NormalListener():
    __tablename__ = 'normallisteners'                   # obbligatorio

    username = Column(String, primary_key=True, foreign_key=User.username)

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<User(username='%s', name='%s', surname='%s',birthdate='%s' password='%s', gender='%s',phone='%d',email='%s')>" % (self.username, self.name, self.surname, self.birthdate, self.password, self.gender, self.phone, self.email)


class PremiumListener():
    __tablename__ = 'premiumlisteners'                   # obbligatorio

    email = Column(String)

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<User(username='%s', name='%s', surname='%s',birthdate='%s' password='%s', gender='%s',phone='%d',email='%s')>" % (self.username, self.name, self.surname, self.birthdate, self.password, self.gender, self.phone, self.email)


class Artist():
    __tablename__ = 'artists'                   # obbligatorio

    email = Column(String)

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<User(username='%s', name='%s', surname='%s',birthdate='%s' password='%s', gender='%s',phone='%d',email='%s')>" % (self.username, self.name, self.surname, self.birthdate, self.password, self.gender, self.phone, self.email)


# SONGS

class Song():
    __tablename__ = 'songs'                   # obbligatorio

    email = Column(String)

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<User(username='%s', name='%s', surname='%s',birthdate='%s' password='%s', gender='%s',phone='%d',email='%s')>" % (self.username, self.name, self.surname, self.birthdate, self.password, self.gender, self.phone, self.email)


class NormalSong():
    __tablename__ = 'normalsongs'                   # obbligatorio

    email = Column(String)

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<User(username='%s', name='%s', surname='%s',birthdate='%s' password='%s', gender='%s',phone='%d',email='%s')>" % (self.username, self.name, self.surname, self.birthdate, self.password, self.gender, self.phone, self.email)


class PremiumSong():
    __tablename__ = 'premiumsongs'                   # obbligatorio

    email = Column(String)

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<User(username='%s', name='%s', surname='%s',birthdate='%s' password='%s', gender='%s',phone='%d',email='%s')>" % (self.username, self.name, self.surname, self.birthdate, self.password, self.gender, self.phone, self.email)
# STATISTICS


class Statistic():
    __tablename__ = 'statistics'                   # obbligatorio

    email = Column(String)

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<User(username='%s', name='%s', surname='%s',birthdate='%s' password='%s', gender='%s',phone='%d',email='%s')>" % (self.username, self.name, self.surname, self.birthdate, self.password, self.gender, self.phone, self.email)


# GENERES

class Genre():
    __tablename__ = 'genres'                   # obbligatorio

    email = Column(String)

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<User(username='%s', name='%s', surname='%s',birthdate='%s' password='%s', gender='%s',phone='%d',email='%s')>" % (self.username, self.name, self.surname, self.birthdate, self.password, self.gender, self.phone, self.email)

# verso artist


class Relate():
    __tablename__ = 'relate'                   # obbligatorio

    email = Column(String)

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<User(username='%s', name='%s', surname='%s',birthdate='%s' password='%s', gender='%s',phone='%d',email='%s')>" % (self.username, self.name, self.surname, self.birthdate, self.password, self.gender, self.phone, self.email)

# verso song


class Belong():
    __tablename__ = 'belong'                   # obbligatorio

    email = Column(String)

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<User(username='%s', name='%s', surname='%s',birthdate='%s' password='%s', gender='%s',phone='%d',email='%s')>" % (self.username, self.name, self.surname, self.birthdate, self.password, self.gender, self.phone, self.email)


# CREATES

class Creates():
    __tablename__ = 'creates'                   # obbligatorio

    email = Column(String)

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<User(username='%s', name='%s', surname='%s',birthdate='%s' password='%s', gender='%s',phone='%d',email='%s')>" % (self.username, self.name, self.surname, self.birthdate, self.password, self.gender, self.phone, self.email)


# ALBUMS

class Album():
    __tablename__ = 'albums'                   # obbligatorio

    email = Column(String)

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<User(username='%s', name='%s', surname='%s',birthdate='%s' password='%s', gender='%s',phone='%d',email='%s')>" % (self.username, self.name, self.surname, self.birthdate, self.password, self.gender, self.phone, self.email)


# PLAYLIST

class Playlist():
    __tablename__ = 'playlists'                   # obbligatorio

    email = Column(String)

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<User(username='%s', name='%s', surname='%s',birthdate='%s' password='%s', gender='%s',phone='%d',email='%s')>" % (self.username, self.name, self.surname, self.birthdate, self.password, self.gender, self.phone, self.email)


#contain in playlist

class Contains():
    __tablename__ = 'contains'                   # obbligatorio

    email = Column(String)

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<User(username='%s', name='%s', surname='%s',birthdate='%s' password='%s', gender='%s',phone='%d',email='%s')>" % (self.username, self.name, self.surname, self.birthdate, self.password, self.gender, self.phone, self.email)
