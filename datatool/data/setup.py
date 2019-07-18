#---------------------------------------------------------------------------------------------------
# Author: Will Fenton
# Date:   May 21 2019

# This sets up the project structure (makes directories, etc.)
# Gets a Last.fm api key from the user
# Generates a config file, and validates existing config files
#---------------------------------------------------------------------------------------------------

import os
import sys
import sqlite3
from configparser import ConfigParser, ExtendedInterpolation
from datatool.data.api_key import get_api_key, validate_api_key
from datatool.data.db_functions import table_exists, add_user, delete_user, update_data

#---------------------------------------------------------------------------------------------------

def setup():
    package_path = os.path.dirname(sys.modules['__main__'].__file__)
    project_path = os.path.abspath(os.path.join(package_path, os.pardir))
    config_path = os.path.join(project_path, "config.ini")

    config_parser = ConfigParser(interpolation=ExtendedInterpolation())

    # validate existing config
    if os.path.exists(config_path):
        config_parser.read(config_path)

        # check that all files exist
        filepaths = [config_parser.get("files", option) for option in config_parser.options("files")]
        for filepath in filepaths:
            assert(os.path.exists(filepath))

        # validate api key
        api_key = config_parser.get("settings", "api_key")
        assert(validate_api_key(api_key))

        # verify that the database exists, ensure that Users and History tables exist
        db_path = config_parser.get("db", "db_path")
        db = sqlite3.connect(db_path)
        for table in ("Users", "History"):
            assert(table_exists(db, table))

        db.close()

    # create config
    else:
        # check whether /Last.fm-Data-Tool/user_data exists, if not create it
        data_path = os.path.join(project_path, "user_data")
        if not os.path.exists(data_path):
            os.mkdir(data_path)

        users_path = os.path.join(data_path, "users")
        if not os.path.exists(users_path):
            os.mkdir(users_path)

        db_path = os.path.join(data_path, "database.db")

        # database exists but no config file
        if os.path.exists(db_path):
            db = sqlite3.connect(db_path)

            for table in ("Users", "History"):
                assert(table_exists(db, table))

            users = [row[0] for row in db.execute("SELECT username FROM Users;")]
            for username in users:
                assert(table_exists(db, f"[user-{user}]"))

        # create database
        else:
            db = sqlite3.connect(db_path)

            # Create tables
            db.execute("CREATE TABLE Users (username TEXT, timestamp INTEGER, PRIMARY KEY (username));")
            db.execute("CREATE TABLE History (username TEXT, timestamp INTEGER, type TEXT, PRIMARY KEY (username, timestamp));")

            db.execute("INSERT INTO History VALUES ('DB', strftime('%s', 'now'), 'DB_CREATED');")

            db.commit()
            db.close()

        api_key = get_api_key()

        config_parser["settings"] = {
            "api_key": api_key
        }

        config_parser["files"] = {
            "project_path": project_path,
            "data_path": "${files:project_path}/user_data",
            "db_path": "${files:data_path}/database.db",
            "users_path": "${files:data_path}/users"
        }

        config_parser["db"] = {
            "db_path": "${files:db_path}"
        }

        with open(config_path, 'w') as f:
            config_parser.write(f)

#---------------------------------------------------------------------------------------------------
