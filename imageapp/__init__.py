# __init__.py is the top level file in a Python package.

from quixote.publish import Publisher

# this imports the class RootDirectory from the file 'root.py'
from .root import RootDirectory
from . import html, image
import sqlite3
import os

def create_publisher():
     p = Publisher(RootDirectory(), display_exceptions='plain')
     p.is_thread_safe = True
     return p
 
def setup():                            # stuff that should be run once.
    html.init_templates()
    if not os.path.exists('./images.sqlite'):
        create_table()

def create_table(): 		
    db = sqlite3.connect('images.sqlite')
    db.execute('CREATE TABLE IF NOT EXISTS image_store \
	            (num INTEGER PRIMARY KEY, image BLOB, format TEXT, name TEXT, description TEXT)');
    db.execute('CREATE TABLE IF NOT EXISTS image_comment (imageId INTEGER, comment TEXT)');
    some_data = open('imageapp/dice.png', 'rb').read()
    image.add_image(some_data, 'png', 'Dice', 'Nice dice!')    
    db.commit()
    db.close()

def teardown():                         # stuff that should be run once.
    pass
