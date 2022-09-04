from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from flask_login import UserMixin
import requests
from datetime import date

from flask_login import current_user

from sqlalchemy.exc import PendingRollbackError

from werkzeug.security import generate_password_hash, check_password_hash

from Codice.database import Session_artist, Session_guestmanager, Session_listener, Session_premiumlistener, Session
from Debug.models import Belong, Genre


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

    def get_current_user():
        return current_user.username

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

    def register_user(temp_session_db,  username, name, surname, birthdate, password, gender, phone, email, artist):
        try:
            temp_password = User.encrypt_password(password)
            user = User(username, name, surname, birthdate,
                        temp_password, gender, phone, email)
            temp_session_db.add(user)
            if artist == 'True':
                artist = Artist(username)
                temp_session_db.add(artist)
            else:
                normal = NormalListener(username)
                temp_session_db.add(normal)
            temp_session_db.commit()
            return True
        except PendingRollbackError as e:
            temp_session_db.rollback()
            return False
        except:
            temp_session_db.flush()
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
        user = User.get_user(temp_session_db, username)
        # print(user)
        temp_session_db.delete(user)
        temp_session_db.commit()

    def move_user_to_premium(username):
        try:
            premiumlistener = PremiumListener(username)
            Session_guestmanager.add(premiumlistener)
            user = NormalListener.get_user(Session_guestmanager, username)
            Session_guestmanager.delete(user)

            Session_guestmanager.commit()
            return True
        except:
            Session_guestmanager.rollback()
            return False

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

    users = relationship(User, backref=backref(
        "normallisteners", cascade="all,  delete, delete-orphan"), uselist=False)

    def __init__(self, username):
        self.username = username

    def get_user(temp_session_db, temp_username):
        user = temp_session_db.query(NormalListener).filter(
            NormalListener.username == temp_username).first()
        return user

    # questo metodo è opzionale, serve solo per pretty printing

    def __repr__(self):
        return "<NormalListener(username='%s')>" % (self.username)


# PREMIUMLISTENERS

class PremiumListener(Base):
    __tablename__ = 'premiumlisteners'                   # obbligatorio

    username = Column(String, ForeignKey(User.username), primary_key=True)

    users = relationship(User, backref=backref(
        "premiumlistenes", cascade="all,  delete, delete-orphan"), uselist=False)

    def __init__(self, username):
        self.username = username

    # questo metodo è opzionale, serve solo per pretty printing

    def __repr__(self):
        return "<PremiumListener(username='%s')>" % (self.username)

# ARTIST


class Artist(Base):
    __tablename__ = 'artists'                   # obbligatorio

    username = Column(String, ForeignKey(User.username), primary_key=True)

    users = relationship(User, backref=backref(
        "artists", cascade="all,  delete, delete-orphan"), uselist=False)

    def __init__(self, username):
        self.username = username

    def insert_song(temp_name, temp_album, temp_cover, temp_releasedate, temp_content, temp_username, song_genres, song_type):
        try:

            song = Song(name=temp_name, idsong=None, album=temp_album, cover=temp_cover,
                        releasedate=temp_releasedate, content=temp_content)
            Session_artist.add(song)
            Session_artist.flush()
            belong = Belong(genre=song_genres, song=song.idsong)
            Session_artist.add(belong)

            if song_type == 'The song will be premium':
                # PremiumSong.register(song.idsong)
                premiumsong = PremiumSong(song=song.idsong)
                Session_artist.add(premiumsong)

            else:
                # NormalSong.register(song.idsong)
                normalsong = NormalSong(song=song.idsong)
                Session_artist.add(normalsong)

            create = Creates(username=temp_username, song=song.idsong)
            Session_artist.add(create)

            Session_artist.commit()
            return True
        except:
            Session_artist.rollback()
            return False

    def check_if_artist(temp_username):
        try:
            artist = Session_artist.query(Artist).filter(
                Artist.username == temp_username).count()
            if artist == 0:
                return 2
            else:
                return 1
        except:
            return 0

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

    artists = relationship(Artist, backref=backref(
        "albums", cascade="all,  delete, delete-orphan"))

    def __init__(self, idalbum, name, cover, artist):
        self.idalbum = idalbum
        self.name = name
        self.cover = cover
        self.artist = artist

    def get_albums(temp_username):
        albums = Session_artist.query(Album).filter(
            Album.artist == temp_username).all()
        return albums

    def get_albums_name(temp_username, albums):
        list_albums = ['']
        if albums is not None:
            for i in albums:
                list_albums.append(i.name)
            return list_albums
        return list_albums

    def extract_cover_album(list_albums, choice):
        try:
            for i in list_albums:
                if i.name == choice:
                    return i.cover
            return None
        except:
            return None
    def extract_id_album(list_albums, choice):
        for i in list_albums:
            if i.name == choice:
                return i.idalbum
        return None

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

    albums = relationship(Album, backref=backref(
        "songs", cascade="all,  delete, delete-orphan"))

    def __init__(self, name, idsong, album, cover, releasedate, content):
        self.name = name
        self.idsong = idsong
        self.album = album
        self.cover = cover
        self.releasedate = releasedate
        self.content = content

    def insert_song(temp_name, temp_album, temp_cover, temp_releasedate, temp_content):
        # Session_artist

        song = Song(name=temp_name, idsong=None, album=temp_album, cover=temp_cover,
                    releasedate=temp_releasedate, content=temp_content)
        return song

    # def get_song_with_artist_genres():
    #
    #    return song

    def get_songs():  # provisoria###############
        songs = Session_artist.query(Song,Belong.genre,Creates.username,Album.name).join(Belong).join(Creates).join(Album).all()
        return songs

    def check_links(cover, content):
        try:
            request_cover = requests.get(cover)
            request_content = requests.get(content)
            if request_cover.status_code == 200 and request_content.status_code == 200:
                return True
            else:
                return False
        except:
            return False
    
    def get_song_playlist(idplaylist):
        songs=Session_artist.query(Song).join(Contains).filter(Contains.list==idplaylist).all()
        return songs

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<Song(name='%s', idsong='%d',album='%d' cover='%s', releaseDate='%s',content='%s')>" % (self.name, self.idsong, self.album, self.cover, self.releasedate, self.content)


# NORMALSONGS

class NormalSong(Base):
    __tablename__ = 'normalsongs'                   # obbligatorio

    song = Column(Integer, ForeignKey(Song.idsong), primary_key=True)

    songs = relationship(Song, backref=backref(
        "normalsongs", cascade="all,  delete, delete-orphan"), uselist=False)

    def __init__(self, song):
        self.song = song

    def get_songs():  # provisoria###############
        songs = Session_listener.query(Song,Belong.genre,Creates.username,Album.name).join(Belong).join(Creates).join(Album).join(NormalSong).all()
        return songs
    # questo metodo è opzionale, serve solo per pretty printing

    def __repr__(self):
        return "<NormalSong(song='%d')>" % (self.song)


# PREMIUMSONGS

class PremiumSong(Base):
    __tablename__ = 'premiumsongs'                   # obbligatorio

    song = Column(Integer, ForeignKey(Song.idsong), primary_key=True)

    songs = relationship(Song, backref=backref(
        "premiumsongs", cascade="all,  delete, delete-orphan"), uselist=False)

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

    songs = relationship(Song, backref=backref(
        "statistics", cascade="all,  delete, delete-orphan"), uselist=False)

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

    list = ['', 'Rock', 'Pop', 'Metal', 'Rap',
            'Classic', 'Jazz', 'Reggae', 'Latin']

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

    genres = relationship(Genre, backref=backref(
        "belong", cascade="all,  delete, delete-orphan"))
    songs = relationship(Song, backref=backref(
        "belong", cascade="all,  delete, delete-orphan"))

    def __init__(self, genre, song):
        self.genre = genre
        self.song = song

    ##########################################################################################################
    # questo metodo è opzionale, serve solo per pretty printing

    def __repr__(self):
        return "<Belong(genre='%s', song='%s')>" % (self.genre, self.song)

# CREATES


class Creates(Base):
    __tablename__ = 'creates'                   # obbligatorio

    song = Column(String,  ForeignKey(Song.idsong), primary_key=True,)
    username = Column(String, ForeignKey(Artist.username), primary_key=True)

    songs = relationship(Song, backref=backref(
        "creates", cascade="all,  delete, delete-orphan"))
    artists = relationship(Artist, backref=backref(
        "creates", cascade="all,  delete, delete-orphan"))

    def __init__(self, username, song):
        self.username = username
        self.song = song

    def check_artist(temp_username):
        user = Session_artist.query(Creates).filter(
            Creates.username == temp_username).count()
        if user > 0:
            return True
        else:
            return False

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

    users = relationship(User, backref=backref(
        "playlists", cascade="all,  delete, delete-orphan"))

    def __init__(self, name,idlist, author, creationdate):
        self.name = name
        self.idlist = idlist
        self.creationdate = creationdate
        self.author = author

    # questo metodo è opzionale, serve solo per pretty printing

    def create(temp_session_db,temp_name,temp_author):
        try:
            playlist=Playlist(name=temp_name,idlist=None,author=temp_author, creationdate=date.today())
            temp_session_db.add(playlist)
            temp_session_db.commit()
            return True
        except:
            temp_session_db.rollback()
            return False

    def get_playlist_user(temp_session_db,temp_author):
        playlists = temp_session_db.query(Playlist).filter(Playlist.author == temp_author).all()
        return playlists

    
    def get_playlist_name_id(temp_username, playlists):
        playlists_names_id = [('','')]
        if playlists is not None:
            for i in playlists:
                id= i.idlist
                name=i.name
                playlists_names_id.append((str(id),name))
        return playlists_names_id
    
    def delete_playlist(idplaylist):
        Session_artist.query(Playlist).filter(Playlist.idlist==idplaylist).delete()
        Session_artist.commit()

    def __repr__(self):
        return "<Playlist(name='%s', idlist='%d', creationdate='%s',author='%s')>" % (self.name, self.idlist, self.creationdate, self.author)


#contain in playlist

class Contains(Base):
    __tablename__ = 'contains'                   # obbligatorio

    song = Column(Integer, ForeignKey(Song.idsong), primary_key=True)
    list = Column(Integer, ForeignKey(Playlist.idlist), primary_key=True)

    songs = relationship(Song, backref=backref(
        "contains", cascade="all,  delete, delete-orphan"))
    playlists = relationship(Playlist, backref=backref(
        "contains", cascade="all,  delete, delete-orphan"))

    def __init__(self, song, list):
        self.song = song
        self.list = list

    def create(songid,playlistid):
        contains=Contains(songid,playlistid)
        Session_artist.add(contains)
        Session_artist.commit()

    def delete_song_from_playlist(idsong,idplaylist):
        Session_artist.query(Contains).filter(Contains.song==idsong,Contains.list==idplaylist).delete()
        Session_artist.commit()
        
    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<Contains(song='%d', list='%d')>" % (self.song, self.list)
