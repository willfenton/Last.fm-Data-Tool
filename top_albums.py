import sqlite3
import datetime

# Connect to database
db_connection = sqlite3.connect("database.db")
cursor = db_connection.cursor()

# Get top albums
cursor.execute("SELECT album_name, artist_name, count(*), min(unix_timestamp) FROM '{}' GROUP BY album_name, artist_name HAVING count(*)>75 ORDER BY min(unix_timestamp) ASC;".format("user-willfenton14"))

albums = []

for row in cursor:
    album = [row[0], row[1], row[2], row[3]]
    readable_date = datetime.datetime.utcfromtimestamp(row[3]).replace(tzinfo=datetime.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S")
    album.append(readable_date)
    albums.append(album)

print("  " + "-" * 116)
print("  |  {:<40}  |  {:<25}  |  {:<5}  |  {:<25}  |".format("Album", "Artist", "Count", "First listened to"))
print("  " + "-" * 116)
for album in albums:
    print("  |  {:<40.40}  |  {:<25.25}  |  {:<5}  |  {:<25.25}  |".format(album[0], album[1], album[2], album[4]))
print("  " + "-" * 116)

