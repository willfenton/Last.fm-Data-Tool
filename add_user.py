# Author : Will Fenton
# Email  : wfenton@ualberta.ca
# Date   : 5 January 2019


import sqlite3
import re


# Get names of all tables
def get_tables(cursor):
    tables = set()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for row in cursor:
        tables.add(row[0])
    return tables


# Get and validate the username
def get_username(cursor):

    # Get existing users
    users = set()
    cursor.execute("SELECT username FROM Users;")
    for row in cursor:
        users.add(row[0])


    # Last.fm usernames between 2-15 characters, begin with a letter, contain only letters, numbers, '-' or '_'
    regex_pattern = "[a-zA-Z]{1}[0-9a-zA-Z_-]{1,14}"

    # Validate username
    while True:
        username = input("Enter your last.fm username: ").lower()
        if re.fullmatch(regex_pattern, username) is None:
            print("That username is invalid.")
        elif username in users:
            print("Table for that user already exists.")
        else:
            break
    print("Username validated")

    return username


# Connect to database
db_connection = sqlite3.connect("database.db")
cursor = db_connection.cursor()

# Get username to add
username = get_username(cursor)

# Add user to "Users" and "History" tables
cursor.execute("INSERT INTO Users VALUES (?, strftime('%s', 'now'));", [username])
cursor.execute("INSERT INTO History VALUES (?, strftime('%s', 'now'), 'CREATED')", [username])

# Add table for user
cursor.execute("CREATE TABLE [user-{}] (unix_timestamp INTEGER, text_timestamp TEXT, artist_name TEXT, artist_mbid TEXT, track_name TEXT, track_mbid TEXT, album_name TEXT, album_mbid TEXT, last_fm_url TEXT, small_image_url TEXT, medium_image_url TEXT, large_image_url TEXT, extralarge_image_url TEXT, image_filename TEXT, PRIMARY KEY (track_name, artist_name, album_name, unix_timestamp));".format(username))

# Commit changes and close connection to database
db_connection.commit()
db_connection.close()
