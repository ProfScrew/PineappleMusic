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

class User(Base, UserMixin):
    __tablename__ = 'users'

    username = Column(String, primary_key=True)
    name = Column(String)
    surname = Column(String)
    birthdate = Column(Date)
    password = Column(String)
    gender = Column(String)
    phone = Column(String)
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

    def encrypt_password(password):
        return generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    # the following three methods are used to get the type of user and the type of user session
    def get_type_user(temp_username): #1 from username returns number referenced type of user
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
            
    def get_type_user_session(temp_username): #2 returns session from  username
        type_user = User.get_type_user(temp_username)
        if type_user == 1:
            return Session_listener
        elif type_user == 2:
            return Session_premiumlistener
        elif type_user == 3:
            return Session_artist
        
    def get_type_user_session_from_number(temp_username, type_user): #3 returns session from number
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

    #used in signup route 
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
        except:
            temp_session_db.rollback()
            return False

    #used in profile route to update account info
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

    #used to delete acount, all the sub info are deleted automaticaly by the database(using cascade)
    def delete_user(username):
        try:
            user = User.get_user(Session_deletemanager,username)
            Session_deletemanager.delete(user)
            Session_deletemanager.commit()
        except:
            Session_deletemanager.rollback()

    #after inserting "card info" user is moved to premium
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

    def __repr__(self):
        return "<User(username='%s', name='%s', surname='%s',birthdate='%s' password='%s', gender='%s',phone='%s',email='%s')>" % (
            self.username, self.name, self.surname, self.birthdate,
            self.password, self.gender, self.phone, self.email)

    def get_id(self):
        return (self.username)



class NormalListener(Base):
    __tablename__ = 'normallisteners'

    username = Column(String, ForeignKey(User.username), primary_key=True)

    users = relationship(User, backref=backref(
        "normallisteners", cascade="all,  delete, delete-orphan"), uselist=False)

    def __init__(self, username):
        self.username = username

    #used to find user in pr 
    def get_user(temp_session_db, temp_username):
        user = temp_session_db.query(NormalListener).filter(
            NormalListener.username == temp_username).first()
        return user

    def __repr__(self):
        return "<NormalListener(username='%s')>" % (self.username)



class PremiumListener(Base):
    __tablename__ = 'premiumlisteners'

    username = Column(String, ForeignKey(User.username), primary_key=True)

    users = relationship(User, backref=backref(
        "premiumlistenes", cascade="all,  delete, delete-orphan"), uselist=False)

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return "<PremiumListener(username='%s')>" % (self.username)



class Artist(Base):
    __tablename__ = 'artists'

    username = Column(String, ForeignKey(User.username), primary_key=True)

    users = relationship(User, backref=backref(
        "artists", cascade="all,  delete, delete-orphan"), uselist=False)

    def __init__(self, username):
        self.username = username

    def insert_album(temp_name, temp_cover, temp_artist):
        try:    
            album = Album(name=temp_name, idalbum=None, cover=temp_cover, artist=temp_artist)
            Session_artist.add(album)
            Session_artist.commit()
            return True
        except:
            Session_artist.rollback()
            return False 
    
    #inserts song in the database and returns confirmation that is later sent to the route
    def insert_song(temp_name, temp_album, temp_cover, temp_releasedate, temp_content, temp_username, song_genres, song_type, temp_session_db):
        try:
            song = Song(name=temp_name, idsong=None, album=temp_album, cover=temp_cover,
                        releasedate=temp_releasedate, content=temp_content)
            temp_session_db.add(song)
            temp_session_db.flush() # used to communicate with the database but information 
                                    # sent are in pending state(waits for commit).
                                    # With that we can get the id of the song
            
            belong = Belong(genre=song_genres, song=song.idsong)
            temp_session_db.add(belong)

            if song_type == 'The song will be premium':
                premiumsong = PremiumSong(song=song.idsong)
                temp_session_db.add(premiumsong)
            else:
                normalsong = NormalSong(song=song.idsong)
                temp_session_db.add(normalsong)

            create = Creates(username=temp_username, song=song.idsong)
            temp_session_db.add(create)

            statistic=Statistic(song = song.idsong, upvote = 0,downvote = 0, views = 0)
            temp_session_db.add(statistic)
            temp_session_db.commit()
            
            return True
        except:
            temp_session_db.rollback()
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
    
    def check_link(temp_link): # the following two functions are used to check if the links are valid
        try:
            request_cover = requests.get(temp_link)
            if request_cover.status_code == 200:
                return True
            else:
                return False
        except:
            return False
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
    
    # used to switch song from normal to premium or viceversa
    def switch_exclusivity(temp_premium, temp_idsong, temp_session_db):
        if temp_premium == 1:   #add premium remove normal
            query = NormalSong(song=temp_idsong)
            temp_session_db.delete(query)
            query = PremiumSong(song=temp_idsong)
            temp_session_db.add(query)
            
        elif temp_premium == 2: #add normal remove premium
            query = PremiumSong(song=temp_idsong)
            temp_session_db.delete(query)
            query = NormalSong(song=temp_idsong)
            temp_session_db.add(query)
    
    # used to modify changed values of a song
    def modify_song(temp_idsong,temp_name,temp_album,temp_cover,temp_content,temp_releasedate, temp_genre, temp_premium, temp_session_db):
        try:
            query_update = []   #the first part checks changes and adds them to the list
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
                temp_session_db.execute(i)
            
            if temp_premium != None:
                Artist.switch_exclusivity(temp_premium, temp_idsong, temp_session_db)
                
            temp_session_db.commit()
            return True
        except:
            temp_session_db.rollback()
            return False
    
    #deletes song from the database linked stuff are deleted automatically by cascade
    def delete_song(temp_idsong,temp_session_db):
        try:
            song = temp_session_db.query(Song).filter(Song.idsong == temp_idsong).first()
            temp_session_db.delete(song)
            temp_session_db.commit()
            return True
        except:
            temp_session_db.rollback()
            return False
    
    #modifies album name and cover, if cover is changed the changes are applied to all songs of the album
    def modify_album(temp_idalbum, temp_name, temp_cover, temp_artist, temp_session_db):
        try:
            if temp_cover == '':
                if not Album.check_artist_album_name(temp_artist,temp_name):            #modifies name
                    query = update(Album).where(Album.idalbum == temp_idalbum).values(name = temp_name)
                else:
                    return False
            else:
                if not Artist.check_link(temp_cover):
                    return False
                album = temp_session_db.query(Album).filter(Album.idalbum == temp_idalbum).first()
                if temp_name == album.name:                                             #modifies cover
                    query = update(Album).where(Album.idalbum == temp_idalbum).values(cover = temp_cover.split("/")[5])
                else:                                                                   #modifies everything
                    if not Album.check_artist_album_name(temp_artist,temp_name):
                        query = update(Album).where(Album.idalbum == temp_idalbum).values(cover = temp_cover.split("/")[5], name = temp_name)
                    else:
                        return False
                    
            temp_session_db.execute(query)
            
            if temp_cover != '':
                Artist.change_cover_album(temp_idalbum, temp_cover.split("/")[5])
            
            temp_session_db.commit()
            return True
        except:
            temp_session_db.rollback()
            return False
    
    #used to change cover of all songs of an album
    def change_cover_album(temp_album, temp_cover,temp_session_db):
        query = update(Song).where(Song.album == temp_album).values(cover = temp_cover)
        temp_session_db.execute(query)
        return
    
    # deletes album and all songs linked to it(cascade)
    def delete_album(temp_idalbum, temp_session_db):
        try:
            album = temp_session_db.query(Album).filter(
                Album.idalbum == temp_idalbum).first()
            temp_session_db.delete(album)
            temp_session_db.commit()
            return True
        except:
            temp_session_db.rollback()
            return False

    def __repr__(self):
        return "<Artist(username='%s')>" % (self.username)


class Album(Base):
    __tablename__ = 'albums'

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

    # checks if an album with the same name already exists for the same artist
    # (artist can't have two or more albums with the same name, but exist different albums with the same name but different artists)
    def check_artist_album_name(temp_username, temp_name):
        album = Session_artist.query(Album).filter(and_( Album.artist == temp_username, Album.name == temp_name)).count()
        if(album>0):
            return True
        else:
            return False 
    
    def get_albums_username(temp_username):
        albums = Session_artist.query(Album).filter(
            Album.artist == temp_username).all()
        return albums
    
    def get_albums_id(temp_idalbum):
        albums = Session_artist.query(Album).filter(
            Album.idalbum == temp_idalbum).first()
        return albums

    #used to extract albums in list format user by a form
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
    
    def extract_cover_album(list_albums, choice):   #extracts cover of the album selected in the select field
        try:
            for i in list_albums:
                if i.name == choice:
                    return i.cover
            return None
        except:
            return None
    def extract_id_album(list_albums, choice):      #extracts id of the album selected in the select field
        for i in list_albums:
            if i.name == choice:
                return i.idalbum
        return None
    
    def __repr__(self):
        return "<Album(idalbum='%d', name='%s', cover='%s',artists='%s')>" % (
            self.idalbum, self.name, self.cover, self.artists)



class Song(Base):
    __tablename__ = 'songs'

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

    # function used to get all songs || songs of a specific genre      
    def get_songs(temp_user, temp_session_db, genre=''):
        try:
            if temp_session_db == Session_listener:                                                 #extracts normal songs
                if genre=='':
                    song_user = temp_session_db.query(Record).filter(Record.user == temp_user).subquery()   #subquery used to extract likes and dislikes of the user
                    songs = temp_session_db.query(Song,Belong.genre,Creates.username,Album.name,song_user).join(Belong).join(Creates).outerjoin(Album).join(NormalSong).outerjoin(song_user).all()
                else:
                    song_user = temp_session_db.query(Record).filter(Record.user == temp_user).subquery()
                    songs = temp_session_db.query(Song,Belong.genre,Creates.username,Album.name,song_user).join(Belong).join(Creates).outerjoin(Album).join(NormalSong).outerjoin(song_user).filter(Belong.genre==genre).all()
            elif temp_session_db == Session_premiumlistener or temp_session_db == Session_artist:   #extracts premium songs
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
    
    # extracts all songs of a specific playlist
    def get_song_playlist(temp_user,idplaylist):
        song_user = Session_artist.query(Record).filter(Record.user == temp_user).subquery()
        songs=Session_artist.query(Song,Belong.genre,Creates.username,Album.name,song_user).join(Belong).join(Creates).outerjoin(Album).join(Contains).outerjoin(song_user).filter(Contains.list==idplaylist).all()
        return songs
    
    #used in homepage to extract the 10 most liked songs
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
    
    #used in homepage to extract the 10 most listened songs
    def get_top_view_songs(temp_session_db, redirect_search = False, temp_user = None):
        
        try:
            if redirect_search: #this part is used for the redirect from homepage 
                if temp_session_db == Session_listener:
                    song_user = temp_session_db.query(Record).filter(Record.user == temp_user).subquery()   #subquery used to extract likes and dislikes of the user
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
            else:               #this part is used for the homepage
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
    
    # used in homepage to extract 10 songs that are suggested to the user based on his likes by genre, 
    # if he doesn't have any likes None is returned(in route is viewed top listened songs again) 
    def get_suggestion_songs(temp_user, temp_session_db, redirect_search = False):
        
        try:        
            #count genre | num liked for each cathegory
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
                    result_query = union(result_query, song)    #union of all the queries
            result = temp_session_db.execute(result_query).all()
            return result
        except:
            temp_session_db.rollback()
            return None
    
    def __repr__(self):
        return "<Song(name='%s', idsong='%d',album='%d' cover='%s', releaseDate='%s',content='%s')>" % (
            self.name, self.idsong, self.album, self.cover, self.releasedate, self.content)



class NormalSong(Base):
    __tablename__ = 'normalsongs'

    song = Column(Integer, ForeignKey(Song.idsong), primary_key=True)

    songs = relationship(Song, backref=backref(
        "normalsongs", cascade="all,  delete, delete-orphan"), uselist=False)

    def __init__(self, song):
        self.song = song

    #check if song is normal
    def check_song(temp_song, temp_session_db):
        temp = temp_session_db.query(NormalSong.song).filter(NormalSong.song == temp_song).first() is not None
        return temp

    def __repr__(self):
        return "<NormalSong(song='%d')>" % (self.song)



class PremiumSong(Base):
    __tablename__ = 'premiumsongs'

    song = Column(Integer, ForeignKey(Song.idsong), primary_key=True)

    songs = relationship(Song, backref=backref(
        "premiumsongs", cascade="all,  delete, delete-orphan"), uselist=False)

    def __init__(self, song):
        self.song = song

    #check if song is premium
    def check_song(temp_song, temp_session_db):
        temp = temp_session_db.query(PremiumSong.song).filter(PremiumSong.song == temp_song).first() is not None
        return temp

    def __repr__(self):
        return "<PremiumSong(song='%d')>" % (self.song)



class Record(Base):
    __tablename__ = 'records'
    
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
    
    # insert record(like or dislike) to database
    def insert(temp_user, temp_song, temp_vote, temp_session_db):
        try:
            record = Record(temp_user,temp_song,temp_vote)
            temp_session_db.add(record)
            temp_session_db.commit()
        except:
            temp_session_db.rollback()
        return
    
    #if user takes down his vote its deleted from database
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

    def __repr__(self):
        return "<Statistic(song='%d', upvote='%d', downvote='%d',views='%d')>" % (
            self.song, self.upvote, self.downvote, self.views)



class Statistic(Base):
    __tablename__ = 'statistics'

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

    #when user clicks a song, views are incremented
    def increase_views(temp_song, temp_session_db):
        try: 
            temp_session_db.execute(update(Statistic).where(Statistic.song == temp_song).values(views= Statistic.views+1))
            temp_session_db.commit()
        except:
            temp_session_db.rollback()

    #get statistics used by artist
    def get_statistics(temp_username, temp_session_db):
        temp = temp_session_db.query(Statistic.upvote,Statistic.downvote,Statistic.views,Song.name).join(Song).join(Creates).filter(Creates.username == temp_username).all()
        return temp
    
    #rivedere se serve <---- non usato
    def insert_statistics(temp_song,temp_session_db):
        try:
            statistic=Statistic(song = temp_song , upvote = 0,downvote = 0, views = 0)
            temp_session_db.add(statistic)
            temp_session_db.commit()
            return True
        except:
            temp_session_db.rollback()
            return False
    
    def __repr__(self):
        return "<Statistic(song='%d', upvote='%d', downvote='%d',views='%d')>" % (self.song, self.upvote, self.downvote, self.views)



class Genre(Base):
    __tablename__ = 'genres'

    name = Column(String, primary_key=True)
    cover = Column(String)


    def __init__(self, name):
        self.name = name

    def get_genres():
        return Session_artist.query(Genre).all()
    #returnts a list of genres used by artist to create songs(later modified in belong functions get_genre_list)
    def get_genre_list_database():
        tuple_list = Genre.get_genres()
        list = ['']
        for genre in tuple_list:
            list.append(genre.name)
        return list


    def __repr__(self):
        return "<Genre(name='%s')>" % (self.name)



class Belong(Base):
    __tablename__ = 'belong'

    genre = Column(String, ForeignKey(Genre.name), primary_key=True)
    song = Column(String, ForeignKey(Song.idsong), primary_key=True)

    genres = relationship(Genre, backref=backref(
        "belong", cascade="all,  delete, delete-orphan"))
    songs = relationship(Song, backref=backref(
        "belong", cascade="all,  delete, delete-orphan"))

    def __init__(self, genre, song):
        self.genre = genre
        self.song = song

    #returns a list of genres and the song genre is on the first position
    def get_genre_list(temp_song_id, temp_session_db):
        list_new = Genre.get_genre_list_database()
        entry = temp_session_db.query(Belong).filter(Belong.song == temp_song_id).first()
        check = False
        forcondition = (b for b in range(len(list_new)) if entry.genre == list_new[b])
        for b in forcondition:
            check = True
            list_new[0] = list_new[b]
            list_new.pop(b)
            list_new.append('')
        if check : list_new.pop(len(list_new)-1 )
        
        return list_new
    
    def __repr__(self):
        return "<Belong(genre='%s', song='%s')>" % (self.genre, self.song)



class Creates(Base):
    __tablename__ = 'creates'

    song = Column(String,  ForeignKey(Song.idsong), primary_key=True,)
    username = Column(String, ForeignKey(Artist.username), primary_key=True)

    songs = relationship(Song, backref=backref(
        "creates", cascade="all,  delete, delete-orphan"))
    artists = relationship(Artist, backref=backref(
        "creates", cascade="all,  delete, delete-orphan"))

    def __init__(self, username, song):
        self.username = username
        self.song = song

    # used during login to check if artist has songs, (if not hes account is deleted(another function))
    def check_artist(temp_username):
        user = Session_deletemanager.query(Creates).filter(
            Creates.username == temp_username).count()
        if user > 0:
            return True
        else:
            return False

    def __repr__(self):
        return "<Creates(song='%s',username='%s')>" % (self.song, self.username)



class Playlist(Base):
    __tablename__ = 'playlists'

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
    
    #create an empty playlist
    def create(temp_session_db,temp_name,temp_author):
        try:
            playlist=Playlist(name=temp_name,idlist=None,author=temp_author, creationdate=date.today())
            temp_session_db.add(playlist)
            temp_session_db.commit()
            return True
        except:
            temp_session_db.rollback()
            return False
    #gets user playlists
    def get_playlist_user(temp_session_db,temp_author):
        playlists = temp_session_db.query(Playlist).filter(Playlist.author == temp_author).all()
        return playlists
    
    #used to create list of playlists in the search page form
    def get_playlist_name_id(temp_username, playlists): 
        playlists_names_id = [('','')]
        if playlists is not None:
            for i in playlists:
                id= i.idlist
                name=i.name
                playlists_names_id.append((str(id),name))
        return playlists_names_id
    
    def delete_playlist(idplaylist,temp_session_db):
        try:
            temp_session_db.query(Playlist).filter(Playlist.idlist==idplaylist).delete()
            temp_session_db.commit()
        except:
            temp_session_db.rollback()

    def __repr__(self):
        return "<Playlist(name='%s', idlist='%d', creationdate='%s',author='%s')>" % (
            self.name, self.idlist, self.creationdate, self.author)



class Contains(Base):   #song contain in playlist
    __tablename__ = 'contains'

    song = Column(Integer, ForeignKey(Song.idsong), primary_key=True)
    list = Column(Integer, ForeignKey(Playlist.idlist), primary_key=True)

    songs = relationship(Song, backref=backref(
        "contains", cascade="all,  delete, delete-orphan"))
    playlists = relationship(Playlist, backref=backref(
        "contains", cascade="all,  delete, delete-orphan"))

    def __init__(self, song, list):
        self.song = song
        self.list = list

    #used to get songs in a playlist
    def create(songid,playlistid, temp_session_db):
        try:
            contains=Contains(songid,playlistid)
            temp_session_db.add(contains)
            temp_session_db.commit()
        except:
            temp_session_db.rollback()
    
    #deletes song from playlist(if playlist is deleted its songs are deleted too by cascade so no need to delete them manualy)
    def delete_song_from_playlist(idsong,idplaylist, temp_session_db):
        try:
            temp_session_db.query(Contains).filter(Contains.song==idsong,Contains.list==idplaylist).delete()
            temp_session_db.commit()
        except:
            temp_session_db.rollback
        
    def __repr__(self):
        return "<Contains(song='%d', list='%d')>" % (self.song, self.list)