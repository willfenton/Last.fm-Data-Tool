import os
import datetime
import sqlite3
from PIL import Image
    

filenames = []

width = 8
height = 8

num_albums = width * height

db = sqlite3.connect("database.db")
for row in db.execute("SELECT album_name, artist_name, image_filename, COUNT(*) FROM 'user-lashinskay' GROUP BY album_name, artist_name, image_filename ORDER BY COUNT(*) DESC LIMIT ?;", [num_albums]).fetchall():
    filenames.append(row[2])

collage = Image.new('RGB', ((width * 300), (height * 300)), color=0)

collage_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "collage")
image_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")

# Pasting album art onto collage
for i in range(num_albums):
    image_path = os.path.join(image_directory, filenames[i])
    x = (i % width) * 300
    y = (i // width) * 300
    img = Image.open(image_path,'r')
    collage.paste(img, (x, y))
    
now = datetime.datetime.now()
timestamp = now.strftime('%Y-%m-%d')
    
collage_path = os.path.join(collage_directory, f"{timestamp}({width}x{height}).png")

collage.save(collage_path)
