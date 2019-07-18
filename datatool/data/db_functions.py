#---------------------------------------------------------------------------------------------------
# Author: Will Fenton
# Date:   July 14 2019

# Database utility functions
#---------------------------------------------------------------------------------------------------

import re
import os
import sys
import sqlite3
import requests
from shutil import rmtree, copyfileobj
from datetime import datetime
from configparser import ConfigParser, ExtendedInterpolation

#---------------------------------------------------------------------------------------------------

# returns the config parser object
def get_config():
    package_path = os.path.dirname(sys.modules['__main__'].__file__)
    project_path = os.path.abspath(os.path.join(package_path, os.pardir))
    config_path = os.path.join(project_path, "config.ini")
    config_parser = ConfigParser(interpolation=ExtendedInterpolation())
    config_parser.read(config_path)
    return config_parser


# validate last.fm username (2-15 chars, start with letter, alphanumeric, '-', '_')
# return True if the given username is a valid last.fm username, False if not
def validate_username(username, api_key):
    username = username.lower()
    match = re.match(r"^[a-zA-Z][a-zA-Z0-9\-_]{1,14}$", username)
    if match is None:
        return False
    api_url = f"http://ws.audioscrobbler.com/2.0/?method=user.getinfo&user={username}&api_key={api_key}&format=json"
    response = requests.get(api_url)
    return response.status_code == 200


# return True if a table with the given name exists in the db, False if not
def table_exists(db, table_name):
    table_names = [table[0] for table in db.execute("SELECT name FROM sqlite_master WHERE type='table';")]
    return table_name in table_names


# create a table for a last.fm user to the database
def add_user(db, username, api_key):
    username = username.lower()

    if not validate_username(username, api_key):
        return False

    if table_exists(db, f"user-{username}"):
        return False

    db.execute(f"CREATE TABLE [user-{username}] (unix_timestamp INTEGER, text_timestamp TEXT, artist_name TEXT, artist_mbid TEXT, track_name TEXT, track_mbid TEXT, album_name TEXT, album_mbid TEXT, last_fm_url TEXT, small_image_url TEXT, medium_image_url TEXT, large_image_url TEXT, extralarge_image_url TEXT, image_path TEXT, PRIMARY KEY (track_name, artist_name, album_name, unix_timestamp));")
    db.execute("INSERT INTO Users VALUES (?, strftime('%s', 'now'));", [username])
    db.execute("INSERT INTO History VALUES (?, strftime('%s', 'now'), 'CREATED');", [username])
    db.commit()

    config_parser = get_config()
    users_path = config_parser.get("files", "users_path")
    user_path = os.path.join(users_path, username)
    os.mkdir(user_path)
    os.mkdir(os.path.join(user_path, "resources"))
    os.mkdir(os.path.join(user_path, "collage"))

    return table_exists(db, f"user-{username}")


# delete a last.fm user from the database
def delete_user(db, username, api_key):
    username = username.lower()

    if not validate_username(username, api_key):
        return False
    
    if not table_exists(db, f"user-{username}"):
        return False

    db.execute(f"DROP TABLE IF EXISTS [user-{username}];")
    db.execute(f"DELETE FROM Users WHERE username='{username}';")
    db.execute("INSERT INTO History VALUES (?, strftime('%s', 'now'), 'DELETED');", [username])
    db.commit()

    config_parser = get_config()
    users_path = config_parser.get("files", "users_path")
    user_path = os.path.join(users_path, username)
    rmtree(user_path)

    return not table_exists(db, f"user-{username}")


# call the last.fm api and download a page of 200 scrobbles
def get_page(username, api_key, page_number):
    api_url = f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={username}&api_key={api_key}&format=json&page={page_number}&limit=200"
    page = requests.get(api_url)
    return page.json()


# get the number of pages of scrobbles (200 scrobbles / page) for a given user
def get_num_pages(username, api_key):
    page = get_page(username, api_key, 1)
    attributes = page["recenttracks"]["@attr"]
    # print("{} scrobbles total ({} pages)".format(attributes["total"], attributes["totalPages"]))
    return int(attributes["totalPages"])


# insert a page of scrobbles into the database
def insert_page(db, username, page, default_image_path, image_directory):
    insert_string = f"INSERT INTO [user-{username}] VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
    regex = re.compile(r"https://.*/i/u/.*/(.*)")
    try:
        tracks = page["recenttracks"]["track"]
        for track in tracks:
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

                try:
                    image_filename = re.search(regex, extralarge_image_url).group(1)
                    image_path = os.path.join(image_directory, image_filename)
                    if not os.path.exists(image_path):
                        response = requests.get(extralarge_image_url, stream=True)
                        with open(image_path, 'wb') as out_file:
                            copyfileobj(response.raw, out_file)
                        del response
                except:
                    image_path = default_image_path

                # print(f"{track_name} by {artist_name}")

                arguments = [unix_timestamp, text_timestamp, artist_name, artist_mbid, track_name, track_mbid, album_name, album_mbid, last_fm_url, small_image_url, medium_image_url, large_image_url, extralarge_image_url, image_path]
                db.execute(insert_string, arguments)
                
            # Either the track is currently playing or scrobble is in the database already
            except Exception as e:
                # print(e)
                pass

    except Exception as e:
        print(e)


# download all new scrobbles for a given user since the last time they were updated
# downloads all scrobbles if it's the first time
def update_data(db, username, api_key):
    username = username.lower()
    try:
        last_update_timestamp = int(db.execute(f"SELECT unix_timestamp FROM [user-{username}] ORDER BY unix_timestamp DESC LIMIT 1;").fetchone()[0])
        readable = datetime.utcfromtimestamp(last_update_timestamp).strftime('%Y-%m-%d %H:%M:%S')
        print(f"Last updated {readable}. Now updating.")        
    except:
        last_update_timestamp = 0
        print("Downloading all data.")

    config_parser = get_config()
    users_path = config_parser.get("files", "users_path")
    user_path = os.path.join(users_path, username)
    resources_path = os.path.join(user_path, "resources")

    project_path = config_parser.get("files", "project_path")
    default_image_path = os.path.join(project_path, "datatool/resources/default.png")

    num_pages = get_num_pages(username, api_key)

    # Download all pages with new scrobbles
    for i in range(1, num_pages + 1):
        print(f"Page {i} of {num_pages}")

        page = get_page(username, api_key, i)

        try:
            first_timestamp = int(page["recenttracks"]["track"][0]["date"]["uts"])
            last_timestamp = int(page["recenttracks"]["track"][len(page["recenttracks"]["track"]) - 1]["date"]["uts"])
        except:
            first_timestamp = int(datetime.now().strftime("%s"))
            last_timestamp = int(datetime.now().strftime("%s"))

        if first_timestamp < last_update_timestamp:
            break
        if last_timestamp < last_update_timestamp:
            insert_page(db, username, page, default_image_path, resources_path)
            break
        insert_page(db, username, page, default_image_path, resources_path)

    new_scrobbles = db.execute(f"SELECT track_name, album_name, artist_name FROM [user-{username}] WHERE unix_timestamp > ? ORDER BY unix_timestamp ASC;", [last_update_timestamp]).fetchall()
    count = len(new_scrobbles)
    for scrobble in new_scrobbles:
        track_name, album_name, artist_name = scrobble
        print(f"{track_name} by {artist_name}")
    print(f"Downloaded {count} new scrobbles.")

    db.execute("INSERT INTO History VALUES (?, strftime('%s', 'now'), 'UPDATED')", [username])
    db.commit()

#---------------------------------------------------------------------------------------------------
