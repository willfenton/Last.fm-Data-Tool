#---------------------------------------------------------------------------------------------------
# Author: Will Fenton
# Date:   July 17 2019

# Creates an album art collage of the user's most listened to albums
#---------------------------------------------------------------------------------------------------

import os
import sys
import sqlite3
from datetime import datetime
from PIL import Image

#---------------------------------------------------------------------------------------------------

def generate_collage(db, username, width=10, height=10, show_collage=False):

    num_albums = width * height

    # get filepaths for the top albums
    image_paths = [row[0] for row in db.execute(f"SELECT image_path, album_name FROM [user-{username}] GROUP BY image_path, album_name ORDER BY COUNT(*) DESC LIMIT ?;", [num_albums])]

    # collage image on which we'll paste the album art
    collage = Image.new('RGB', ((width * 300), (height * 300)), color=0)

    # Pasting album art onto collage
    for i in range(num_albums):
        x = (i % width) * 300
        y = (i // width) * 300
        album_art = Image.open(image_paths[i], 'r')
        collage.paste(album_art, (x, y))
        
    timestamp = datetime.now().strftime('%Y-%m-%d')

    # determine path to save the collage
    package_path = os.path.dirname(sys.modules['__main__'].__file__)
    project_path = os.path.abspath(os.path.join(package_path, os.pardir))
    collage_path = os.path.join(project_path, f"user_data/users/{username}/collage/{timestamp} ({width}x{height}).png")
        
    # save the collage
    collage.save(collage_path)

    if show_collage:
        collage.show(title=f"Top Album Collage ({width}x{height})")

#---------------------------------------------------------------------------------------------------
