#!/usr/bin/python3
# Author : Will Fenton
# Email  : wfenton@ualberta.ca
# Date   : 5 January 2019


import sqlite3
import requests
import re
import os
import shutil
from datetime import datetime


def get_page(username, page_number, api_key):

    # Url to request
    api_url = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={}&api_key={}&format=json&page={}&limit=200".format(username, api_key, page_number)

    # Get page
    page = requests.get(api_url)

    # Convert response to json
    json = page.json()

    return json


def get_num_pages(username, api_key):

    # Get a page
    page = get_page(username, 1, api_key)

    # Attributes total # of scrobbles and total # of pages
    attributes = page["recenttracks"]["@attr"]

    # Print info
    print("{} scrobbles total ({} pages)".format(attributes["total"], attributes["totalPages"]))

    return int(attributes["totalPages"])


def get_all_pages(username):

    # Read api key from file
    file = open("apikey.txt", "r")
    api_key = file.read()
    file.close()

    # Determine number of pages to download
    num_pages = get_num_pages(username, api_key)

    pages = []

    # Download all pages
    for i in range(1, num_pages+1):
        print("Page {} of {}".format(i, num_pages))
        page = get_page(username, i, api_key)
        pages.append(page)

    return pages


def get_new_pages(username, last_update_timestamp):

    # Read api key from file
    file = open("apikey.txt", "r")
    api_key = file.read()
    file.close()

    # Determine total number of pages
    num_pages = get_num_pages(username, api_key)

    pages = []

    # Download all pages with new scrobbles
    for i in range(1, num_pages+1):
        page = get_page(username, i, api_key)

        print(len(pages))

        try:
            first_timestamp = int(page["recenttracks"]["track"][0]["date"]["uts"])
        except:
            first_timestamp = int(datetime.utcnow().strftime("%s"))

        last_timestamp = int(page["recenttracks"]["track"][len(page["recenttracks"]["track"]) - 1]["date"]["uts"])

        if first_timestamp < last_update_timestamp:
            print(".1")
            return pages
        if last_timestamp < last_update_timestamp:
            print(".2")
            pages.append(page)
            return pages

        pages.append(page)

    return pages

# Connect to database
db_connection = sqlite3.connect("database.db")
cursor = db_connection.cursor()

# Get all usernames
usernames = []
cursor.execute("SELECT username FROM Users;")
for row in cursor:
    usernames.append(row[0])

# Print all usernames
print("Select a user:")
for i in range(len(usernames)):
    print("{}. {}".format(i + 1, usernames[i]))

# Select username
user_input = int(input())
while user_input not in range(1, len(usernames) + 1):
    print("Invalid option.")
    user_input = int(input())
username = usernames[user_input - 1]

insert_string = "INSERT INTO [user-{}] VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);".format(username)

# Find timestamp of last update
cursor.execute("SELECT timestamp FROM History WHERE username=? AND type=? ORDER BY timestamp DESC LIMIT 1;", [username, "UPDATE"])

try:
    last_update_timestamp = int(cursor.fetchone()[0])
    readable = datetime.utcfromtimestamp(last_update_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    print("Last updated {}. Now updating.".format(readable))

    pages = get_new_pages(username, last_update_timestamp)

except:
    pages = get_all_pages(username)

new_scrobbles = 0

image_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")

for page in pages:
    try:
        tracks = page["recenttracks"]["track"]
        for track in tracks:
            # Extract scrobble data and insert record into database
            try:
                unix_timestamp = track["date"]["uts"]
                text_timestamp = track["date"]["#text"]

                artist_name = track["artist"]["#text"]
                artist_mbid = track["artist"]["mbid"]

                track_name = track["name"]
                track_mbid = track["mbid"]

                album_name = track["album"]["#text"]
                album_mbid = track["album"]["mbid"]

                last_fm_url = track["url"]

                small_image_url = track["image"][0]["#text"]
                medium_image_url = track["image"][1]["#text"]
                large_image_url = track["image"][2]["#text"]
                extralarge_image_url = track["image"][3]["#text"]

                image_filename = re.search("https://(.*)/i/u/(.*)/(.*)", extralarge_image_url).group(3)

                image_path = os.path.join(image_directory, image_filename)

                if not os.path.exists(image_path):
                    response = requests.get(extralarge_image_url, stream=True)
                    with open(image_path, 'wb') as out_file:
                        shutil.copyfileobj(response.raw, out_file)
                    del response

                arguments = [unix_timestamp, text_timestamp, artist_name, artist_mbid, track_name, track_mbid, album_name, album_mbid, last_fm_url, small_image_url, medium_image_url, large_image_url, extralarge_image_url, image_filename]

                # Insert into database
                cursor.execute(insert_string, arguments)

                # Successfully added new scrobble to database
                new_scrobbles += 1

            # Either track is currently playing or scrobble is in the database already
            except Exception as e:
                print(e)
    except:
        pass

# Record update
cursor.execute("INSERT INTO History VALUES (?, strftime('%s', 'now'), 'UPDATE')", [username])

print("Added {} new scrobbles.".format(new_scrobbles))

# Commit changes and close connection to database
db_connection.commit()
db_connection.close()
