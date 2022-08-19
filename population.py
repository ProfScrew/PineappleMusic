#
#requirements:
#
#pip install sqlalchemy, names, random_words
#
#program populates database with random entries
#

import datetime
import email
import string
from unicodedata import name
from unittest import result
import sqlalchemy as db
from sqlalchemy import *
import names
import random

#fills genres table with the ten popular genres
def fill_generes(engine, connection, metadata):
    genres_list =  ["Pop", "Rap", "Rock", "Dance and Electronic", "Latin", "Indie", "Classic", "K-Pop", "Country", "Metal"]
    genres_table = db.Table('genres', metadata, autoload=True, autoload_with=engine)
    
    for x in genres_list:
        query = db.insert(genres_table).values(genre = x)
        connection.execute(query)
        
        
def get_random_date():
    start_date = datetime.date(1900,1,1)
    end_date = datetime.date.today()
    
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    
    return(random_date)

#assigns user to one of the three subclasses normalListener, premiumListener, artist

def assign_user(connection, metadata, assign_number, username):
    if assign_number == 1:
        assign_type = 'normallisteners'
    elif assign_number ==2:
        assign_type = 'premiumlisteners'
    elif assign_number == 3:
        assign_type = 'artists'
    assign_table = db.Table(assign_type, metadata, autoload=True, autoload_with=engine)
    
    query_insert = db.insert(assign_table).values(username = username)
    connection.execute(query_insert)


#fills users table with entries and checks so it doesnt have doubles
def fill_users(engine, connection, metadata, number_users):
    
    switch_user = 1
    users_table = db.Table('users', metadata, Column('username', String, primary_key=True),
                                 Column('name', String),
                                 Column('surname', String),
                                 Column('datebirth', Date),
                                 Column('password', String),
                                 Column('gender', String),
                                 Column('phone', Integer),
                                 Column('email', String)
                                 )
    
    for x in range(number_users):
        
        #gender sort
        
        temp_gender_choice = random.randint(0,1)
        if temp_gender_choice == 1:
            temp_gender_name = 'male'
            temp_gender = 'M'
        else:
            temp_gender_name = 'female'
            temp_gender = 'F'
         
        #get name
        temp_name = names.get_first_name(temp_gender_name)
        temp_surname = names.get_last_name()
        
        #username generation
        check_username = True
        while check_username == True:
            random_number = random.randint(0,9999)
            temp_username = temp_name + temp_surname + str(random_number)
            
            query_check_username = db.select([users_table.columns.username]).where(users_table.columns.username == temp_username)
            result_temp = connection.execute(query_check_username)
            result_row = result_temp.fetchone()
            
            #print(type(result_row))
            #checks if the username already exists if yes changes the random number
            if type(result_row) == type(None):
                check_username = False
        
        temp_email = temp_username + '@gmail.com'
        
        #generates phone and checks if someone else is using it, it yes generates another    
            
        check_phone = True
        while check_phone:
            temp_phone = random.randint(1000000,9999999)
            query_check_phone = db.select([users_table.columns.phone]).where(users_table.columns.phone == temp_phone)
            
            result_temp = connection.execute(query_check_phone)
            result_row = result_temp.fetchone()
            
            if type(result_row) == type(None):
                check_phone = False
        
        
        temp_datebirth = get_random_date()
        
        ####################################
        # insertion in database
        
        query_insert = db.insert(users_table).values(username = temp_username,
                                                     name = temp_name,
                                                     surname = temp_surname,
                                                     datebirth = temp_datebirth,
                                                     password = 'password',
                                                     gender = temp_gender,
                                                     phone = temp_phone,
                                                     email = temp_email
        )
        
        connection.execute(query_insert)
        
        if switch_user == 3:
            switch_user = 1
        else:
            switch_user += 1

        assign_user(connection, metadata, switch_user,temp_username)

#############################

#deb fill_songs():

###################


engine = db.create_engine('postgresql://admin:ciao@localhost:5432/Stupify', echo = True)
connection = engine.connect()
metadata = MetaData()

fill_users(engine, connection, metadata, 3)




# #users = db.Table('users', metadata, autoload=True, autoload_with=engine)
# users = db.Table('users', metadata, Column('username', String, primary_key=True),
#                                  Column('name', String),
#                                  Column('surname', String),
#                                  Column('datebirth', Date),
#                                  Column('password', String),
#                                  Column('gender', String),
#                                  Column('phone', Integer),
#                                  Column('email', String)
#                                  )


# query = db.select([users])

# resultP = connection.execute(query)

# resultS = resultP.fetchall()
# print(resultS)

######
#Menu#
######