CREATE TABLE Users
(
  Username VARCHAR(40) NOT NULL,
  Name VARCHAR(20) NOT NULL,
  Surname VARCHAR(20) NOT NULL,
  Birthdate DATE NOT NULL,
  Password VARCHAR(20) NOT NULL CHECK(LENGTH(Password)>=8),
  Gender CHAR(1) NOT NULL CHECK(Gender = 'F' OR Gender = 'M'),
  Phone INT NOT NULL,
  Email VARCHAR(40) NOT NULL UNIQUE,
  PRIMARY KEY (Username)
);

CREATE TABLE NormalListeners
(
  Username VARCHAR(40) NOT NULL,
  PRIMARY KEY (Username),
  FOREIGN KEY (Username) REFERENCES Users(Username)
);

CREATE TABLE PremiumListeners
(
  Username VARCHAR(40) NOT NULL,
  PRIMARY KEY (Username),
  FOREIGN KEY (Username) REFERENCES Users(Username)
);

CREATE TABLE Artists
(
  Username VARCHAR(40) NOT NULL,
  PRIMARY KEY (Username),
  FOREIGN KEY (Username) REFERENCES Users(Username)
);

CREATE TABLE Albums(
  IDAlbum INT NOT NULL,
  Name VARCHAR(40) NOT NULL,
  Cover VARCHAR(40),
  Artist VARCHAR(40) NOT NULL,

  PRIMARY KEY (IDAlbum),
  FOREIGN KEY (Artist) REFERENCES Artists(Username)
);

CREATE TABLE Songs
(
  Name VARCHAR(40) NOT NULL,
  IDSong INT NOT NULL,
  Album INT,
  Cover VARCHAR(40),
  ReleaseDate DATE NOT NULL,
  Content VARCHAR(80),
  PRIMARY KEY (IDSong),
  FOREIGN KEY (Album) REFERENCES Albums(IDAlbum)
);



CREATE TABLE NormalSongs
(
  Song INT NOT NULL,
  PRIMARY KEY (Song),
  FOREIGN KEY (Song) REFERENCES Songs(IDSong)
);

CREATE TABLE PremiumSongs
(
  ExpiryDate INT NOT NULL,
  Song INT NOT NULL,
  PRIMARY KEY (Song),
  FOREIGN KEY (Song) REFERENCES Songs(IDSong)
);

CREATE TABLE Statistics
(
  Song INT NOT NULL,
  Upvote INT NOT NULL,
  Downvote INT NOT NULL,
  Views INT NOT NULL,
  FOREIGN KEY (Song) REFERENCES Songs(IDSong)
);

CREATE TABLE Playlists
(
  Name VARCHAR(20) NOT NULL,
  IDList INT NOT NULL,
  CreationDate DATE NOT NULL,
  Author VARCHAR(40) NOT NULL,
  PRIMARY KEY (IDList),
  FOREIGN KEY (Author) REFERENCES Users(Username)
);

CREATE TABLE Contains
(
  Song INT NOT NULL,
  List INT NOT NULL,
  PRIMARY KEY (Song, List),
  FOREIGN KEY (Song) REFERENCES Songs(IDSong),
  FOREIGN KEY (List) REFERENCES Playlists(IDList)
);

CREATE TABLE Genres
(
  Name VARCHAR(20) NOT NULL,
  PRIMARY KEY (Name)
);

CREATE TABLE Relate
(
  Genre VARCHAR(20) NOT NULL,
  Artist VARCHAR(40) NOT NULL,
  PRIMARY KEY (Genre, Artist),
  FOREIGN KEY (Genre) REFERENCES Genres(Name),
  FOREIGN KEY (Artist) REFERENCES Artists(Username)
);

CREATE TABLE Belong
(
  Song INT NOT NULL,
  Genre VARCHAR(20) NOT NULL,
  PRIMARY KEY (Song, Genre),
  FOREIGN KEY (Song) REFERENCES Songs(IDSong),
  FOREIGN KEY (Genre) REFERENCES Genres(Name)
);

CREATE TABLE Creates
(
  Song INT NOT NULL,
  Username VARCHAR(40) NOT NULL,
  PRIMARY KEY (Song, Username),
  FOREIGN KEY (Song) REFERENCES Songs(IDSong),
  FOREIGN KEY (Username) REFERENCES Artists(Username)
);
