from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from flask_login import UserMixin


from werkzeug.security import generate_password_hash, check_password_hash

from Codice.database import Session_artist, Session_guestmanager, Session_listener, Session_premiumlistener, Session

Base = declarative_base()
Base.query = Session.query_property()
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

    def scream():
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

    def encrypt_password(password):
        return generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def get_type_user(temp_username):

        if Session_guestmanager.query(NormalListener).filter(NormalListener.username == temp_username).count() == 1:
            return 1
        elif Session_guestmanager.query(PremiumListener).filter(PremiumListener.username == temp_username).count() == 1:
            return 2
        elif Session_guestmanager.query(Artist).filter(Artist.username == temp_username).count() == 1:
            return 3
        else:
            raise Exception("User not in any list")

    def get_type_user_session(temp_username):

        type_user = User.get_type_user(temp_username)
        if type_user == 1:
            return Session_listener
        elif type_user == 2:
            return Session_premiumlistener
        elif type_user == 3:
            return Session_artist

    def get_user(temp_session_db, username):
        user = temp_session_db.query(User).filter(
            User.username == username).first()
        return user

    def register_user(temp_session_db,  username, name, surname, birthdate, password, gender, phone, email):
        try:
            temp_password = User.encrypt_password(password)
            user = User(username, name, surname, birthdate,
                        temp_password, gender, phone, email)
            temp_session_db.add(user)
            temp_session_db.commit()
            return True
        except:
            return False

    def update_user(temp_session_db, temp_username, temp_name, temp_surname, temp_birthdate, temp_password, temp_phone, temp_email, check_password):
        try:
            if check_password:
                query = update(User).where(User.username == temp_username).values(name=temp_name, surname=temp_surname,
                                                                                  birthdate=temp_birthdate, password=temp_password,
                                                                                  phone=temp_phone, email=temp_email)

            else:
                query = update(User).where(User.username == temp_username).values(name=temp_name, surname=temp_surname,
                                                                                  birthdate=temp_birthdate, phone=temp_phone,
                                                                                  email=temp_email)
            temp_session_db.execute(query)
            temp_session_db.commit()
            return True
        except:
            return False

    def delete_user(temp_session_db, username):
        User.scream()
        user = User.get_user(temp_session_db, username)
        User.scream()
        print(user)
        temp_session_db.delete(user)
        temp_session_db.commit()

    # questo metodo è opzionale, serve solo per pretty printing

    def __repr__(self):
        return "<User(username='%s', name='%s', surname='%s',birthdate='%s' password='%s', gender='%s',phone='%d',email='%s')>" % (self.username, self.name, self.surname, self.birthdate, self.password, self.gender, self.phone, self.email)

    # def verify_password(password):
    #    return True

    # def verify_password(self,password):
    #    if self.password == password:
    #        return True
    #    else:
    #        return False

    def get_id(self):
        return (self.username)

# NORMALLISTENER


class NormalListener(Base):
    __tablename__ = 'normallisteners'                   # obbligatorio

    username = Column(String, ForeignKey(User.username), primary_key=True)

    users = relationship(User, backref=backref("normallisteners", cascade="all,  delete, delete-orphan"),
                         cascade="all, delete", uselist=False)

    def __init__(self, username):
        self.username = username

    def register_normallistener(temp_session_db, username):
        try:
            normalistener = NormalListener(username)
            temp_session_db.add(normalistener)
            temp_session_db.commit()
            return True
        except:
            return False

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<NormalListener(username='%s')>" % (self.username)


# PREMIUMLISTENERS

class PremiumListener(Base):
    __tablename__ = 'premiumlisteners'                   # obbligatorio

    username = Column(String, ForeignKey(User.username), primary_key=True)

    users = relationship(User, backref=backref("premiumlistenes", cascade="all,  delete, delete-orphan"), uselist=False)

    def __init__(self, username):
        self.username = username

    def register_premiumlistener(temp_session_db, username):
        try:
            premiumlistener = PremiumListener(username)
            temp_session_db.add(premiumlistener)
            temp_session_db.commit()
            return True
        except:
            return False

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<PremiumListener(username='%s')>" % (self.username)

# ARTIST


class Artist(Base):
    __tablename__ = 'artists'                   # obbligatorio

    username = Column(String, ForeignKey(User.username), primary_key=True)

    users = relationship(User, backref=backref("artists", cascade="all,  delete, delete-orphan"), uselist=False)

    def __init__(self, username):
        self.username = username

    def register_artist(temp_session_db, username):
        try:
            artist = Artist(username)
            temp_session_db.add(artist)
            temp_session_db.commit()
            return True
        except:
            return False

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

    artists = relationship(Artist, backref=backref("albums", cascade="all,  delete, delete-orphan"))

    def __init__(self, idalbum, name, cover, artist):
        self.idalbum = idalbum
        self.name = name
        self.cover = cover
        self.artist = artist

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        # artist o artists?
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

    albums = relationship(Album, backref=backref("songs", cascade="all,  delete, delete-orphan"))

    def __init__(self, name, idsong, album, cover, releasedata, content):
        self.name = name
        self.idsong = idsong
        self.album = album
        self.cover = cover
        self.releasedate = releasedata
        self.content = content

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<Song(name='%s', idsong='%d',album='%d' cover='%s', releaseDate='%s',content='%s')>" % (self.name, self.idsong, self.album, self.cover, self.releasedate, self.content)


# NORMALSONGS

class NormalSong(Base):
    __tablename__ = 'normalsongs'                   # obbligatorio

    song = Column(Integer, ForeignKey(Song.idsong), primary_key=True)

    songs = relationship(Song, backref=backref("normalsongs", cascade="all,  delete, delete-orphan"), uselist=False)

    def __init__(self, song):
        self.song = song

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<NormalSong(song='%d')>" % (self.song)


# PREMIUMSONGS

class PremiumSong(Base):
    __tablename__ = 'premiumsongs'                   # obbligatorio

    song = Column(Integer, ForeignKey(Song.idsong), primary_key=True)

    songs = relationship(Song, backref=backref("premiumsongs", cascade="all,  delete, delete-orphan"), uselist=False)

    def __init__(self, song):
        self.song = song

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

    songs = relationship(Song, backref=backref("statistics", cascade="all,  delete, delete-orphan"), uselist=False)

    def __init__(self, song, upvote, downvote, views):
        self.song = song
        self.upvote = upvote
        self.downvote = downvote
        self.views = views

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<Statistic(song='%d', upvote='%d', downvote='%d',views='%d')>" % (self.song, self.upvote, self.downvote, self.views)


# GENERES

class Genre(Base):
    __tablename__ = 'genres'                   # obbligatorio

    name = Column(String, primary_key=True)

    def __init__(self, name):
        self.name = name

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<Genre(name='%s')>" % (self.name)

# verso artist


'''
class Relate(Base):
    __tablename__ = 'relate'                   # obbligatorio

    genre = Column(String, ForeignKey(Genre.name), primary_key=True)
    artist = Column(String, ForeignKey(Artist.username), primary_key=True)

    genres = relationship(Genre, backref="relate")
    artists = relationship(Artist, backref="relate")

    def __init__(self, genre, artist):
        self.genre = genre
        self.artist = artist

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<Relate(genre='%s', artist='%s')>" % (self.genre, self.artist)
'''
# verso song


class Belong(Base):
    __tablename__ = 'belong'                   # obbligatorio

    genre = Column(String, ForeignKey(Genre.name), primary_key=True)
    song = Column(String, ForeignKey(Song.idsong), primary_key=True)

    genres = relationship(Genre, backref=backref("belong", cascade="all,  delete, delete-orphan"))
    songs = relationship(Song, backref=backref("belong", cascade="all,  delete, delete-orphan"))

    def __init__(self, genre, song):
        self.genre = genre
        self.song = song

    # questo metodo è opzionale, serve solo per pretty printing

    def __repr__(self):
        return "<Belong(genre='%s', song='%s')>" % (self.genre, self.song)

# CREATES


class Creates(Base):
    __tablename__ = 'creates'                   # obbligatorio

    song = Column(String,  ForeignKey(Song.idsong), primary_key=True,)
    username = Column(String, ForeignKey(Artist.username), primary_key=True)

    songs = relationship(Song, backref=backref("creates", cascade="all,  delete, delete-orphan"))
    artists = relationship(Artist, backref=backref("creates", cascade="all,  delete, delete-orphan"))

    def __init__(self, username, song):
        self.username = username
        self.song = song

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

    users = relationship(User, backref=backref("playlists", cascade="all,  delete, delete-orphan"))

    def __init__(self, idlist, creationdate, author):
        self.idlist = idlist
        self.creationdate = creationdate
        self.author = author

    # questo metodo è opzionale, serve solo per pretty printing

    def __repr__(self):
        return "<Playlist(name='%s', idlist='%d', creationdate='%s',author='%s')>" % (self.name, self.idlist, self.creationdate, self.author)


#contain in playlist

class Contains(Base):
    __tablename__ = 'contains'                   # obbligatorio

    song = Column(Integer, ForeignKey(Song.idsong), primary_key=True)
    list = Column(Integer, ForeignKey(Playlist.idlist), primary_key=True)

    songs = relationship(Song,backref=backref("contains", cascade="all,  delete, delete-orphan"))
    playlists = relationship(Playlist, backref=backref("contains", cascade="all,  delete, delete-orphan"))

    def __init__(self, song, list):
        self.song = song
        self.list = list

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<Contains(song='%d', list='%d')>" % (self.song, self.list)
