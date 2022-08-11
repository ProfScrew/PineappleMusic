from platform import release
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

# NORMALLISTENER


class NormalListener():
    __tablename__ = 'normallisteners'                   # obbligatorio

    username = Column(String, primary_key=True, foreign_key=User.username)

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<NormalListener(username='%s')>" % (self.username)


# PREMIUMLISTENERS

class PremiumListener():
    __tablename__ = 'premiumlisteners'                   # obbligatorio

    username = Column(String, primary_key=True, foreign_key=User.username)

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<PremiumListener(username='%s')>" % (self.username)

# ARTIST


class Artist():
    __tablename__ = 'artists'                   # obbligatorio

    username = Column(String, primary_key=True, foreign_key=User.username)

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<Artist(username='%s')>" % (self.username)

# ALBUMS


class Album():
    __tablename__ = 'albums'                   # obbligatorio

    idalbum = Column(Integer, primary_key=True)
    name = Column(String)
    cover = Column(String)
    artists = Column(String, foreign_key=Artist.username)

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<Album(idalbum='%d', name='%s', cover='%s',artists='%s')>" % (self.idalbum, self.name, self.cover, self.artists)

# SONGS


class Song():
    __tablename__ = 'songs'                   # obbligatorio

    name = Column(String)
    idsong = Column(Integer, primary_key=True)
    album = Column(Integer, foreign_key=Album.idalbum)
    cover = Column(String)
    releasedate = Column(Date)
    content = Column(String)

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<Song(name='%s', idsong='%d',album='%d' cover='%s', releaseDate='%s',content='%s')>" % (self.name, self.idsong, self.album, self.cover, self.releasedate, self.content)


# NORMALSONGS

class NormalSong():
    __tablename__ = 'normalsongs'                   # obbligatorio

    song = Column(Integer, primary_key=True, foreign_key=Song.idsong)

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<NormalSong(song='%d')>" % (self.song)


# PREMIUMSONGS

class PremiumSong():
    __tablename__ = 'premiumsongs'                   # obbligatorio

    song = Column(Integer, primary_key=True, foreign_key=Song.idsong)

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<PremiumSong(song='%d')>" % (self.song)


# STATISTICS

class Statistic():
    __tablename__ = 'statistics'                   # obbligatorio

    song = Column(Integer, foreign_key=Song.idsong)
    upvote = Column(Integer)
    downvote = Column(Integer)
    views = Column(Integer)

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<Statistic(song='%d', upvote='%d', downvote='%d',views='%d')>" % (self.song, self.upvote, self.downvote, self.views)


# GENERES

class Genre():
    __tablename__ = 'genres'                   # obbligatorio

    name = Column(String, primary_key=True)

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<Genre(name='%s')>" % (self.name)

# verso artist


class Relate():
    __tablename__ = 'relate'                   # obbligatorio

    genre = Column(String, primary_key=True, foreign_key=Genre.name)
    artist = Column(String, primary_key=True, foreign_key=Artist.username)

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<Relate(genre='%s', artist='%s')>" % (self.genre, self.artist)

# verso song


class Belong():
    __tablename__ = 'belong'                   # obbligatorio

    genre = Column(String, primary_key=True, foreign_key=Genre.name)
    artist = Column(String, primary_key=True, foreign_key=Artist.username)

    # questo metodo è opzionale, serve solo per pretty printing

    def __repr__(self):
        return "<Belong(genre='%s', artist='%s')>" % (self.genre, self.artist)

# CREATES


class Creates():
    __tablename__ = 'creates'                   # obbligatorio

    song = Column(String, primary_key=True, foreign_key=Song.idsong)
    username = Column(String, primary_key=True, foreign_key=Artist.username)

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<Creates(song='%s',username='%s')>" % (self.song, self.username)


# PLAYLIST

class Playlist():
    __tablename__ = 'playlists'                   # obbligatorio

    name = Column(String)
    idlist = Column(Integer, primary_key=True)
    creationdate = Column(Date)
    author = Column(String, foreign_key=User.username)

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<Playlist(name='%s', idlist='%d', creationdate='%s',author='%s')>" % (self.name, self.idlist, self.creationdate, self.author)


#contain in playlist

class Contains():
    __tablename__ = 'contains'                   # obbligatorio

    song = Column(Integer, primary_key=True, foreign_key=Song.idsong)
    list = Column(Integer, primary_key=True, foreign_key=Playlist.idlist)

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<Contains(song='%d', list='%d')>" % (self.song, self.list)
