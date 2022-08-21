from this import d
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

from Codice import Base

# USERS

# tabella = classe che eredita da Base
class User(Base, UserMixin):
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


    
    def __init__(self, username, name, surname, birthdate, password, gender, phone, email):
        self.username = username
        self.name = name
        self.surname = surname
        self.birthdate = birthdate
        self.password = password
        self.gender = gender
        self.phone = phone
        self.email = email
    
    # questo metodo è opzionale, serve solo per pretty printing

    
    
    def __repr__(self):
        return "<User(username='%s', name='%s', surname='%s',birthdate='%s' password='%s', gender='%s',phone='%d',email='%s')>" % (self.username, self.name, self.surname, self.birthdate, self.password, self.gender, self.phone, self.email)

#    @property
#    def password(self):
#        raise AttributeError('password is not a readable attribute')
    
#    @password.setter
#    def password(self,password):
#        self.password = generate_password_hash(password)
    
#    def verify_password(self, password):
#        return check_password_hash(self.password, password)
    
    def verify_password(password):
        return True
        
    def get_id(self):
        return (self.username)
    
# NORMALLISTENER


class NormalListener(Base):
    __tablename__ = 'normallisteners'                   # obbligatorio

    username = Column(String, ForeignKey(User.username), primary_key=True)

    users = relationship(User, backref="normallisteners", uselist=False)

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<NormalListener(username='%s')>" % (self.username)


# PREMIUMLISTENERS

class PremiumListener(Base):
    __tablename__ = 'premiumlisteners'                   # obbligatorio

    username = Column(String, ForeignKey(User.username), primary_key=True)

    users = relationship(User, backref="premiumlistenes", uselist=False)

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<PremiumListener(username='%s')>" % (self.username)

# ARTIST


class Artist(Base):
    __tablename__ = 'artists'                   # obbligatorio

    username = Column(String, ForeignKey(User.username), primary_key=True)

    users = relationship(User, backref="artists", uselist=False)

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<Artist(username='%s')>" % (self.username)

# ALBUMS


class Album(Base):
    __tablename__ = 'albums'                   # obbligatorio

    idalbum = Column(Integer, primary_key=True)
    name = Column(String)
    cover = Column(String)
    artist = Column(String, ForeignKey(Artist.username))

    artists = relationship(Artist, backref="albums")

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<Album(idalbum='%d', name='%s', cover='%s',artists='%s')>" % (self.idalbum, self.name, self.cover, self.artists)

# SONGS


class Song(Base):
    __tablename__ = 'songs'                   # obbligatorio

    name = Column(String)
    idsong = Column(Integer, primary_key=True)
    album = Column(Integer, ForeignKey(Album.idalbum))
    cover = Column(String)
    releasedate = Column(Date)
    content = Column(String)

    albums = relationship(Album, backref="songs")

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<Song(name='%s', idsong='%d',album='%d' cover='%s', releaseDate='%s',content='%s')>" % (self.name, self.idsong, self.album, self.cover, self.releasedate, self.content)


# NORMALSONGS

class NormalSong(Base):
    __tablename__ = 'normalsongs'                   # obbligatorio

    song = Column(Integer, ForeignKey(Song.idsong), primary_key=True)

    songs = relationship(Song, backref="normalsongs", uselist=False)

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<NormalSong(song='%d')>" % (self.song)


# PREMIUMSONGS

class PremiumSong(Base):
    __tablename__ = 'premiumsongs'                   # obbligatorio

    song = Column(Integer, ForeignKey(Song.idsong), primary_key=True)

    songs = relationship(Song, backref="premiumsongs", uselist=False)

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<PremiumSong(song='%d')>" % (self.song)


# STATISTICS

class Statistic(Base):
    __tablename__ = 'statistics'                   # obbligatorio

    song = Column(Integer, ForeignKey(Song.idsong), primary_key=True)
    upvote = Column(Integer)
    downvote = Column(Integer)
    views = Column(Integer)

    songs = relationship(Song, backref="statistics", uselist=False)

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<Statistic(song='%d', upvote='%d', downvote='%d',views='%d')>" % (self.song, self.upvote, self.downvote, self.views)


# GENERES

class Genre(Base):
    __tablename__ = 'genres'                   # obbligatorio

    name = Column(String, primary_key=True)

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<Genre(name='%s')>" % (self.name)

# verso artist


class Relate(Base):
    __tablename__ = 'relate'                   # obbligatorio

    genre = Column(String, ForeignKey(Genre.name), primary_key=True)
    artist = Column(String, ForeignKey(Artist.username), primary_key=True)

    genres = relationship(Genre, backref="relate")
    artists = relationship(Artist, backref="relate")

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<Relate(genre='%s', artist='%s')>" % (self.genre, self.artist)

# verso song


class Belong(Base):
    __tablename__ = 'belong'                   # obbligatorio

    genre = Column(String, ForeignKey(Genre.name), primary_key=True)
    song = Column(String, ForeignKey(Song.idsong), primary_key=True)

    genres = relationship(Genre, backref="belong")
    songs = relationship(Song, backref="belong")

    # questo metodo è opzionale, serve solo per pretty printing

    def __repr__(self):
        return "<Belong(genre='%s', song='%s')>" % (self.genre, self.song)

# CREATES


class Creates(Base):
    __tablename__ = 'creates'                   # obbligatorio

    song = Column(String,  ForeignKey(Song.idsong), primary_key=True,)
    username = Column(String, ForeignKey(Artist.username), primary_key=True)

    songs = relationship(Song, backref="creates")
    artists = relationship(Artist, backref="creates")

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<Creates(song='%s',username='%s')>" % (self.song, self.username)


# PLAYLIST

class Playlist(Base):
    __tablename__ = 'playlists'                   # obbligatorio

    name = Column(String)
    idlist = Column(Integer, primary_key=True)
    creationdate = Column(Date)
    author = Column(String, ForeignKey(User.username))

    users = relationship(User, backref="playlists")

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<Playlist(name='%s', idlist='%d', creationdate='%s',author='%s')>" % (self.name, self.idlist, self.creationdate, self.author)


#contain in playlist

class Contains(Base):
    __tablename__ = 'contains'                   # obbligatorio

    song = Column(Integer, ForeignKey(Song.idsong), primary_key=True)
    list = Column(Integer, ForeignKey(Playlist.idlist), primary_key=True)

    songs = relationship(Song, backref="contains")
    playlists = relationship(Playlist, backref="contains")

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<Contains(song='%d', list='%d')>" % (self.song, self.list)
