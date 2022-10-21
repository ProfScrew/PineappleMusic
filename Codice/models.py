

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.exc import PendingRollbackError, IntegrityError

from sqlalchemy.sql.functions import count
from sqlalchemy.sql.expression import update

from flask_login import UserMixin
from flask import flash

import requests
from datetime import date

from flask_login import current_user

from werkzeug.security import generate_password_hash, check_password_hash

from Codice.database import Session_artist, Session_deletemanager, Session_guestmanager, Session_listener, Session_premiumlistener, Session


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
    
    #account = None
    
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
        try:
            if Session_guestmanager.query(NormalListener).filter(NormalListener.username == temp_username).count() == 1:
                num = 1
            elif Session_guestmanager.query(PremiumListener).filter(PremiumListener.username == temp_username).count() == 1:
                num = 2
            elif Session_guestmanager.query(Artist).filter(Artist.username == temp_username).count() == 1:
                num = 3
            else:
                num = 0
            return num
        except:
            Session_guestmanager.rollback()
            
    #rivedere se uso, altrimenti buttare via
    def get_type_user_session(temp_username):
        type_user = User.get_type_user(temp_username)
        if type_user == 1:
            return Session_listener
        elif type_user == 2:
            return Session_premiumlistener
        elif type_user == 3:
            return Session_artist
    ####
        
    def get_type_user_session_from_number(temp_username, type_user):

        if type_user == 1:
            return Session_listener
        elif type_user == 2:
            return Session_premiumlistener
        elif type_user == 3:
            return Session_artist
    
    def get_user(temp_session_db, username):
        try:
            user = temp_session_db.query(User).filter(
                User.username == username).first()

            return user
        except:
            temp_session_db.rollback()

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
        except IntegrityError:
            temp_session_db.rollback()
            flash("User or email Already in use")
            return False
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
            temp_session_db.rollback()
            return False

    def delete_user(username):
        try:
            user = User.get_user(Session_deletemanager,username)
            # print(user)
            Session_deletemanager.delete(user)
            Session_deletemanager.commit()
        except:
            Session_deletemanager.rollback()

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

    ###rivedere perche
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

    def insert_album(temp_name, temp_cover, temp_artist):
        try:    
            album = Album.insert_album(temp_name, temp_cover, temp_artist)
            Session_artist.add(album)
            Session_artist.commit()
            return True
        except:
            Session_artist.rollback()
            return False
        
    
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

            statistic=Statistic(song = song.idsong, upvote = 0,downvote = 0, views = 0)
            Session_artist.add(statistic)
            
            Session_artist.commit()
            return True
        except:
            Session_artist.rollback()
            return False

    def check_if_artist(temp_username): #usato nel insert song fouri
        try:
            artist = Session_artist.query(Artist).filter(
                Artist.username == temp_username).count()
            Session_artist.commit()
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

    def insert_album(temp_name, temp_cover, temp_artist):
        album = Album(name=temp_name, idalbum=None, cover=temp_cover,
                    artist=temp_artist)
        return album

    def check_artist_album_name(temp_username, temp_name):
        album = Session_artist.query(Album).filter(and_( Album.artist == temp_username, Album.name == temp_name)).count()
        if(album>0):
            return True
        else:
            return False 
        
    def check_link(temp_link):
        try:
            request_cover = requests.get(temp_link)
            if request_cover.status_code == 200:
                return True
            else:
                return False
        except:
            return False
    
    def get_albums(temp_username):
        albums = Session_artist.query(Album).filter(
            Album.artist == temp_username).all()
        return albums
    
    def get_albums_id(temp_idalbum):
        albums = Session_artist.query(Album).filter(
            Album.idalbum == temp_idalbum).first()
        return albums

    def get_albums_name(temp_username, albums, choice):
        list_albums = ['']
        if albums is not None:      #list used in select field by artist
            for i in albums:
                list_albums.append(i.name)
            if choice != None:      #song has already an album so choice is automaticaly selected in the select field
                choice_query = Album.get_albums_id(choice)
                forcondition = (b for b in range(len(list_albums)) if choice_query.name == list_albums[b])
                for b in forcondition:
                    list_albums[0] = list_albums[b]
                    list_albums.pop(b)
                    list_albums.append('')
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
    
    def modify_album(temp_idalbum, temp_name, temp_cover, temp_artist):
        try:
            if temp_cover == '':
                if not Album.check_artist_album_name(temp_artist,temp_name):#modifica nome
                    query = update(Album).where(Album.idalbum == temp_idalbum).values(name = temp_name)
                else:
                    return False
            else:
                if not Album.check_link(temp_cover):
                    return False
                album = Session_artist.query(Album).filter(Album.idalbum == temp_idalbum).first()
                if temp_name == album.name:#modifica cover
                    query = update(Album).where(Album.idalbum == temp_idalbum).values(cover = temp_cover.split("/")[5])
                    #Song.change_cover_album(temp_idalbum, temp_cover.split("/")[5])
                else:#modifica tutto
                    if not Album.check_artist_album_name(temp_artist,temp_name):
                        query = update(Album).where(Album.idalbum == temp_idalbum).values(cover = temp_cover.split("/")[5], name = temp_name)
                        #
                    else:
                        return False
                    
            Session_artist.execute(query)
            
            if temp_cover != '':
                Song.change_cover_album(temp_idalbum, temp_cover.split("/")[5])
            
            Session_artist.commit()
            return True
        except:
            Session_artist.rollback()
            return False
    
    def delete_album(temp_idalbum):
        try:
            album = Session_artist.query(Album).filter(
                Album.idalbum == temp_idalbum).first()
            Session_artist.delete(album)
            Session_artist.commit()
            return True
        except:
            Session_artist.rollback()
            return False

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

    def switch_exclusivity(temp_premium, temp_idsong):#session artist dentro
        if temp_premium == 1:   #add premium remove normal
            query = NormalSong(song=temp_idsong)
            Session_artist.delete(query)
            query = PremiumSong(song=temp_idsong)
            Session_artist.add(query)
            
        elif temp_premium == 2: #add normal remove premium
            query = PremiumSong(song=temp_idsong)
            Session_artist.delete(query)
            query = NormalSong(song=temp_idsong)
            Session_artist.add(query)
            
            

    def modify_song(temp_idsong,temp_name,temp_album,temp_cover,temp_content,temp_releasedate, temp_genre, temp_premium):
        try:
            query_update = []
            if temp_name != None:
                query_update.append(update(Song).where(Song.idsong == temp_idsong).values(name = temp_name))
            if temp_album == -1:
                query_update.append(update(Song).where(Song.idsong == temp_idsong).values(album=None))
            elif temp_album != None:
                query_update.append(update(Song).where(Song.idsong == temp_idsong).values(album=temp_album))
            if temp_cover != None:
                query_update.append(update(Song).where(Song.idsong == temp_idsong).values(cover = temp_cover))
            if temp_content != None:
                query_update.append(update(Song).where(Song.idsong == temp_idsong).values(content = temp_content))
            if temp_releasedate != None:
                query_update.append(update(Song).where(Song.idsong == temp_idsong).values(releasedate = temp_releasedate))
            if temp_genre != None:
                query_update.append(update(Belong).where(Belong.song == temp_idsong).values(genre = temp_genre))
             
            for i in query_update:
                Session_artist.execute(i)
            
            if temp_premium != None:
                Song.switch_exclusivity(temp_premium)
                
            Session_artist.commit()
            return True
        except:
            Session_artist.rollback()
            return False
    
    
    def change_cover_album(temp_album, temp_cover):
        query = update(Song).where(Song.album == temp_album).values(cover = temp_cover)
        Session_artist.execute(query)
        return
    
    # def get_song_with_artist_genres():
    #
    #    return song

    def get_songs(temp_user, temp_session_db, genre=''):  # provisoria###############
        try:
            if temp_session_db == Session_listener:
                if genre=='':
                    song_user = temp_session_db.query(Record).filter(Record.user == temp_user).subquery()   #sotto query per estrarre like
                    songs = temp_session_db.query(Song,Belong.genre,Creates.username,Album.name,song_user).join(Belong).join(Creates).outerjoin(Album).join(NormalSong).outerjoin(song_user).all()
                else:
                    song_user = temp_session_db.query(Record).filter(Record.user == temp_user).subquery()
                    songs = temp_session_db.query(Song,Belong.genre,Creates.username,Album.name,song_user).join(Belong).join(Creates).outerjoin(Album).join(NormalSong).outerjoin(song_user).filter(Belong.genre==genre).all()
            elif temp_session_db == Session_premiumlistener or temp_session_db == Session_artist:
                if genre=='':
                    song_user = temp_session_db.query(Record).filter(Record.user == temp_user).subquery()
                    songs = temp_session_db.query(Song,Belong.genre,Creates.username,Album.name,song_user).join(Belong).join(Creates).outerjoin(Album).outerjoin(song_user).all()
                else:
                    song_user = temp_session_db.query(Record).filter(Record.user == temp_user).subquery()
                    songs = temp_session_db.query(Song,Belong.genre,Creates.username,Album.name,song_user).join(Belong).join(Creates).outerjoin(Album).outerjoin(song_user).filter(Belong.genre==genre).all()
            return songs
        except:
            temp_session_db.rollback()
            return None

    def get_songs_artist(temp_artist):
        temp = Session_artist.query(Song).join(Creates).filter(Creates.username == temp_artist).all()
        return temp
    
    def get_song_id(temp_idsong):
        temp = Session_artist.query(Song).filter(Song.idsong == temp_idsong).first()
        return temp
    
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
    
    def get_song_playlist(temp_user,idplaylist):
        song_user = Session_artist.query(Record).filter(Record.user == temp_user).subquery()
        songs=Session_artist.query(Song,Belong.genre,Creates.username,Album.name,song_user).join(Belong).join(Creates).outerjoin(Album).join(Contains).outerjoin(song_user).filter(Contains.list==idplaylist).all()
        return songs

    def delete_song(temp_idsong):
        try:
            song = Session_artist.query(Song).filter(Song.idsong == temp_idsong).first()
            Session_artist.delete(song)
            Session_artist.commit()
            return True
        except:
            Session_artist.rollback()
            return False
    
    def get_top_like_songs(temp_session_db, redirect_search = False, temp_user = None):
        try:
            if redirect_search:
                if temp_session_db == Session_listener: #this part is used for the redirect from homepage
                    song_user = temp_session_db.query(Record).filter(Record.user == temp_user).subquery()
                    songs = temp_session_db.query(Song,
                                                Belong.genre,
                                                Creates.username,
                                                Album.name,
                                                song_user).join(Belong).join(Creates).outerjoin(Album).join(NormalSong).join(Statistic).outerjoin(song_user).order_by(desc(Statistic.upvote)).limit(10).all()
                    
                elif temp_session_db == Session_premiumlistener or temp_session_db == Session_artist:
                    song_user = temp_session_db.query(Record).filter(Record.user == temp_user).subquery()
                    songs = temp_session_db.query(Song,
                                                Belong.genre,
                                                Creates.username,
                                                Album.name,
                                                song_user).join(Belong).join(Creates).outerjoin(Album).join(Statistic).outerjoin(song_user).order_by(desc(Statistic.upvote)).limit(10).all()
            else:
                if temp_session_db == Session_listener:
                    songs = temp_session_db.query(Song.name.label("name"),
                                                Song.cover.label("cover"),
                                                Belong.genre.label("genre"),
                                                Creates.username.label("artist"),
                                                Album.name.label("album"),
                                                Statistic.upvote.label("likes")).join(Belong).join(Creates).outerjoin(Album).join(NormalSong).join(Statistic).order_by(desc(Statistic.upvote)).limit(10).all()
                    
                elif temp_session_db == Session_premiumlistener or temp_session_db == Session_artist:
                    songs = temp_session_db.query(Song.name.label("name"),
                                                Song.cover.label("cover"),
                                                Belong.genre.label("genre"),
                                                Creates.username.label("artist"),
                                                Album.name.label("album"),
                                                Statistic.upvote.label("likes")).join(Belong).join(Creates).outerjoin(Album).join(Statistic).order_by(desc(Statistic.upvote)).limit(10).all()
            
            return songs
        except:
            temp_session_db.rollback()
            return None
        
    def get_top_view_songs(temp_session_db, redirect_search = False, temp_user = None):
        
        try:
            if redirect_search: #this part is used for the redirect from homepage 
                if temp_session_db == Session_listener:
                    song_user = temp_session_db.query(Record).filter(Record.user == temp_user).subquery()
                    songs = temp_session_db.query(Song,
                                                Belong.genre,
                                                Creates.username,
                                                Album.name,
                                                song_user).join(Belong).join(Creates).outerjoin(Album).join(NormalSong).join(Statistic).outerjoin(song_user).order_by(desc(Statistic.views)).limit(10).all()
                elif temp_session_db == Session_premiumlistener or temp_session_db == Session_artist:
                    song_user = temp_session_db.query(Record).filter(Record.user == temp_user).subquery()
                    songs = temp_session_db.query(Song,
                                                    Belong.genre,
                                                    Creates.username,
                                                    Album.name,
                                                    song_user).join(Belong).join(Creates).outerjoin(Album).join(Statistic).outerjoin(song_user).order_by(desc(Statistic.views)).limit(10).all()
            else:
                if temp_session_db == Session_listener:
                    songs = temp_session_db.query(Song.name.label("name"),
                                                Song.cover.label("cover"),
                                                Belong.genre.label("genre"),
                                                Creates.username.label("artist"),
                                                Album.name.label("album"),
                                                Statistic.views.label("views")).join(Belong).join(Creates).outerjoin(Album).join(NormalSong).join(Statistic).order_by(desc(Statistic.views)).limit(10).all()
                elif temp_session_db == Session_premiumlistener or temp_session_db == Session_artist:
                    songs = temp_session_db.query(Song.name.label("name"),
                                                    Song.cover.label("cover"),
                                                    Belong.genre.label("genre"),
                                                    Creates.username.label("artist"),
                                                    Album.name.label("album"),
                                                    Statistic.views.label("views")).join(Belong).join(Creates).outerjoin(Album).join(Statistic).order_by(desc(Statistic.views)).limit(10).all()
                    
            
            return songs
        except:
            temp_session_db.rollback()
            return None
    
    def get_suggestion_songs(temp_user, temp_session_db, redirect_search = False):
        
        try:        
            #count genre | num liked in this cathegory
            if temp_session_db == Session_listener:
                count_of_genre = temp_session_db.query(Genre.name.label("genre"),
                                                       count(Record.song).label("likes")).join(Belong).join(Song).join(Record).join(NormalSong).filter(and_(Record.vote == True,
                                                                                                                                                            Record.user == temp_user)).order_by(desc("likes")).group_by(Genre.name).limit(10).all()
            elif temp_session_db == Session_premiumlistener or temp_session_db == Session_artist:
                count_of_genre = temp_session_db.query(Genre.name.label("genre"),
                                                       count(Record.song).label("likes")).join(Belong).join(Song).join(Record).filter(and_(Record.vote == True,
                                                                                                                                           Record.user == temp_user)).order_by(desc("likes")).group_by(Genre.name).limit(10).all()
                
            
            if count_of_genre == []:
                return None
            
            total_likes = 0
            for i in count_of_genre:
                total_likes = total_likes + i.likes
                
            arr = []
            for i in count_of_genre:    #determine percentage of song to show per genre
                temp = round(((i.likes * 100) / total_likes)/10)
                if temp != 0:
                    col = []
                    col.append(i.genre)
                    col.append(temp)
                    arr.append(col)
                
            for i in arr:   #extract songs per each genre
                if redirect_search:
                    if temp_session_db == Session_listener:
                        song_user = temp_session_db.query(Record).filter(Record.user == temp_user).subquery()
                        song = temp_session_db.query(Song,
                                                        Belong.genre,
                                                        Creates.username,
                                                        Album.name,
                                                        song_user).join(Belong).join(Creates).outerjoin(Album).join(NormalSong).join(Statistic).outerjoin(song_user).order_by(desc(Statistic.views)).filter(Belong.genre == i[0]).limit(i[1])
                        
                    elif temp_session_db == Session_premiumlistener or temp_session_db == Session_artist:
                        song_user = temp_session_db.query(Record).filter(Record.user == temp_user).subquery()
                        song = temp_session_db.query(Song,
                                                    Belong.genre,
                                                    Creates.username,
                                                    Album.name,
                                                    song_user).join(Belong).join(Creates).outerjoin(Album).join(Statistic).outerjoin(song_user).order_by(desc(Statistic.views)).filter(Belong.genre == i[0]).limit(i[1])
                else:
                    if temp_session_db == Session_listener:
                        song = temp_session_db.query(Song.name.label("name"),
                                                        Song.cover.label("cover"),
                                                        Belong.genre.label("genre"),
                                                        Creates.username.label("artist"),
                                                        Album.name.label("album"),
                                                        Statistic.views.label("views")).join(Belong).join(Creates).outerjoin(Album).join(NormalSong).join(Statistic).order_by(desc(Statistic.views)).filter(Belong.genre == i[0]).limit(i[1])
                        
                    elif temp_session_db == Session_premiumlistener or temp_session_db == Session_artist:
                        song = temp_session_db.query(Song.name.label("name"),
                                                    Song.cover.label("cover"),
                                                    Belong.genre.label("genre"),
                                                    Creates.username.label("artist"),
                                                    Album.name.label("album"),
                                                    Statistic.views.label("views")).join(Belong).join(Creates).outerjoin(Album).join(Statistic).order_by(desc(Statistic.views)).filter(Belong.genre == i[0]).limit(i[1])
                if i == arr[0]:
                    result_query = song
                else:
                    result_query = union(result_query, song)
            result = temp_session_db.execute(result_query).all()
            return result
        except:
            temp_session_db.rollback()
            return None
    
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

    def check_song(temp_song):
        temp = Session_artist.query(NormalSong.song).filter(NormalSong.song == temp_song).first() is not None
        return temp
         
    
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

    def check_song(temp_song):
        temp = Session_artist.query(PremiumSong.song).filter(PremiumSong.song == temp_song).first() is not None
        return temp
    
    # questo metodo è opzionale, serve solo per pretty printing

    def __repr__(self):
        return "<PremiumSong(song='%d')>" % (self.song)


# RECORDS

class Record(Base):
    __tablename__ = 'records'                   # obbligatorio
    
    user = Column(String, ForeignKey(User.username), primary_key=True)
    song = Column(Integer, ForeignKey(Song.idsong), primary_key=True)
    vote = Column(Boolean)
    
    users = relationship(User, backref=backref(
        "users", cascade="all,  delete, delete-orphan"), uselist=False)
    songs = relationship(Song, backref=backref(
        "songs", cascade="all,  delete, delete-orphan"), uselist=False)

    def __init__(self,user, song, vote):
        self.user = user
        self.song = song
        self.vote = vote

    
    
    def insert(temp_user, temp_song, temp_vote, temp_session_db):
        try:
            record = Record(temp_user,temp_song,temp_vote)
            temp_session_db.add(record)
            temp_session_db.commit()
        except:
            temp_session_db.rollback()
        return
    def delete(temp_user, temp_song, temp_session_db):
        try:
            record = temp_session_db.query(Record).filter(and_(Record.user == temp_user, Record.song == temp_song)).first()
            if record != None:
                temp_session_db.delete(record)
            temp_session_db.commit()
            return 
        except:
            temp_session_db.rollback()
            return 

    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<Statistic(song='%d', upvote='%d', downvote='%d',views='%d')>" % (self.song, self.upvote, self.downvote, self.views)


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

    def increase_views(temp_song, temp_session_db):
        try:    
            #update(Song).where(Song.idsong == temp_idsong).values(album=temp_album)
            
            temp_session_db.execute(update(Statistic).where(Statistic.song == temp_song).values(views= Statistic.views+1))
            #   temp_session_db.query(Statistic).filter_by().update({})
            
            #   session.query(Tag).filter_by(tag_id=5).update({'count': Tag.count + 1})
            temp_session_db.commit()
        except:
            temp_session_db.rollback()

    def get_statistics(temp_username):
        temp = Session_artist.query(Statistic.upvote,Statistic.downvote,Statistic.views,Song.name).join(Song).join(Creates).filter(Creates.username == temp_username).all()
        return temp
    
    #rivedere se serve
    def insert_statistics(temp_song):
        try:
            statistic=Statistic(song = temp_song , upvote = 0,downvote = 0, views = 0)
            Session_artist.add(statistic)
            Session_artist.commit()
            return True
        except:
            Session_artist.rollback()
            return False
        
        return
    
    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<Statistic(song='%d', upvote='%d', downvote='%d',views='%d')>" % (self.song, self.upvote, self.downvote, self.views)



# GENERES

class Genre(Base):
    __tablename__ = 'genres'                   # obbligatorio

    name = Column(String, primary_key=True)
    cover = Column(String)

    list = ['', 'Rock', 'Pop', 'Metal', 'Rap',
            'Classic', 'Jazz', 'Reggae', 'Latin']

    def __init__(self, name):
        self.name = name

    def get_genres():
        return Session_artist.query(Genre).all()

    
    
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

    def get_genre_list(temp_song_id): ###rivedere funzione
        list_new = Genre.list.copy()
        entry = Session_artist.query(Belong).filter(Belong.song == temp_song_id).first()
        check = False
        forcondition = (b for b in range(len(list_new)) if entry.genre == list_new[b])
        for b in forcondition:
            check = True
            list_new[0] = list_new[b]
            list_new.pop(b)
            list_new.append('')
        if check : list_new.pop(len(list_new)-1 )
        
        return list_new
    
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
        try:
            contains=Contains(songid,playlistid)
            Session_artist.add(contains)
            Session_artist.commit()
        except:
            Session_artist.rollback()

    def delete_song_from_playlist(idsong,idplaylist):
        Session_artist.query(Contains).filter(Contains.song==idsong,Contains.list==idplaylist).delete()
        Session_artist.commit()
        
    # questo metodo è opzionale, serve solo per pretty printing
    def __repr__(self):
        return "<Contains(song='%d', list='%d')>" % (self.song, self.list)
