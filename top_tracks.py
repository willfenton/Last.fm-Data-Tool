import sqlite3
import datetime

# Connect to database
db_connection = sqlite3.connect("database.db")
cursor = db_connection.cursor()

# Get top albums
cursor.execute("SELECT track_name, album_name, artist_name, count(*), min(unix_timestamp) FROM '{}' GROUP BY track_name, album_name, artist_name HAVING count(*)>10 ORDER BY min(unix_timestamp) ASC;".format("user-willfenton14"))

albums = []

for row in cursor:
    album = [row[0], row[1], row[2], row[3], row[4]]
    readable_date = datetime.datetime.utcfromtimestamp(row[4]).replace(tzinfo=datetime.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S")
    album.append(readable_date)
    albums.append(album)

print("-" * 151)
print("|  {:45}  |  {:30}  |  {:20}  |  {:5}  |  {:25}  |".format("Track", "Album", "Artist", "Count", "First listened to"))
print("-" * 151)
for album in albums:
    print("|  {:45.45}  |  {:30.30}  |  {:20.20}  |  {:<5}  |  {:25.25}  |".format(album[0], album[1], album[2], album[3], album[5]))
print("-" * 151)
