# Author : Will Fenton
# Email  : wfenton@ualberta.ca
# Date   : 3 January 2019


import sqlite3


# Connect to database
db_connection = sqlite3.connect("database.db")
cursor = db_connection.cursor()

# Get all existing tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
num_tables = len(tables)

# Tables already exist, give user options
if num_tables > 0:

    # Print all tables
    print("\nExisting tables:")
    for table in tables:
        print(table[0])
    print()

    # User options
    print("1. Drop all tables and setup")
    print("2. Delete a user")
    print("3. Exit")

    # Get user input
    user_input = input()
    while user_input not in ("1", "2", "3"):
        print("Invalid option.")
        user_input = input()

    # Drop all tables and setup
    if user_input == "1":

        # Drop all tables
        cursor.execute("SELECT 'DROP TABLE ' || name || ';' FROM sqlite_master WHERE TYPE='table';")
        for row in cursor.fetchall():
            cursor.execute(row[0])

        # Create tables
        cursor.execute("CREATE TABLE Users (username TEXT, timestamp INTEGER, PRIMARY KEY (username));")
        cursor.execute("CREATE TABLE History (username TEXT, timestamp INTEGER, type TEXT, PRIMARY KEY (username, timestamp));")

    # Delete a user
    elif user_input == "2":

        # Get list of users
        users = []
        cursor.execute("SELECT username FROM Users;")
        for row in cursor:
            users.append(row[0])

        print()
        print("Select a user to delete.")

        # Display all usernames
        for i in range(len(users)):
            print("{}. {}".format(i + 1, users[i]))

        # Get user input
        user_input = int(input())
        while user_input not in range(1, len(users) + 1):
            print("Invalid option.")
            user_input = int(input())

        user_to_delete = users[user_input - 1]

        # Drop all tables / rows related to that user
        cursor.execute("DROP TABLE IF EXISTS [user-{}];".format(user_to_delete))
        cursor.execute("DELETE FROM Users WHERE username='{}'".format(user_to_delete))
        cursor.execute("DELETE FROM History WHERE username='{}'".format(user_to_delete))

    # Exit
    elif user_input == "3":
        pass

# Fresh database
else:
    # Create tables
    cursor.execute("CREATE TABLE Users (username TEXT, timestamp INTEGER, PRIMARY KEY (username));")
    cursor.execute("CREATE TABLE History (username TEXT, timestamp INTEGER, type TEXT, PRIMARY KEY (username, timestamp));")

# Commit changes and close connection
db_connection.commit()
db_connection.close()
