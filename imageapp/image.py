# image handling API
import sqlite3
from PIL import ImageFile, Image
import os
from StringIO import StringIO

ThumbnailSize = 70, 70
DefaultThumbnail = "dice.png"
image_number = 0

def add_image(data, format, name, description):
    global image_number
    image_number += 1
    db = sqlite3.connect('images.sqlite')
    c = db.cursor()
    c.execute('SELECT num FROM image_store ORDER BY num DESC LIMIT 1')
    row = c.fetchone()
    
    if row == None:
    	index = 0
    else:
    	index = row[0]+1
    
    db.text_factory = bytes
    vars = (index, data, format, name, description)
    db.execute('INSERT INTO image_store VALUES (?,?,?,?,?)', vars)
    
    db.commit()
    db.close()

    return index

def get_image(num):
    db = sqlite3.connect('images.sqlite')
    db.text_factory = bytes
    c = db.cursor()
    c.execute('SELECT image, format, name, description FROM image_store WHERE num = ? LIMIT 1', (num, ))
    result = c.fetchone()
    db.close()
    return result

def get_latest_image():
    db = sqlite3.connect('images.sqlite')
    db.text_factory = bytes
    c = db.cursor()
    c.execute('SELECT image, format, name, description FROM image_store ORDER BY num DESC LIMIT 1')
    result = c.fetchone()
    db.close()
    return result

def get_images_by_metadata(name, descrip):
    db = sqlite3.connect('images.sqlite')
    c = db.cursor()
    c.execute('SELECT num, name, description FROM image_store WHERE name LIKE \'%{0}%\' AND description LIKE \'%{1}%\''.format(name, descrip))
    return [dict(num=row[0],name=row[1],description=row[2]) for row in c.fetchall()]

def get_all_indexes():
    result = []
    db = sqlite3.connect('images.sqlite')
    db.text_factory = bytes
    c = db.cursor()
    c.execute('SELECT num FROM image_store ORDER BY num ASC')
    for row in c:
	result.append(row[0])

    return result

def get_all_images():
    images = {}
    images['results'] = []
    db = sqlite3.connect('images.sqlite')
    c = db.cursor()

    c.execute('SELECT num, name, description FROM image_store ORDER BY num ASC')
    for row in c:
        result = {'index':row[0], 'name':row[1], 'desc':row[2]}
        images['results'].append(result) 
    db.close()
    print images
    return images

def search(name, description):
    images = {}
    images['results'] = []
    db = sqlite3.connect('images.sqlite')
    c = db.cursor()

    c.execute('SELECT num, name, description FROM image_store WHERE name LIKE ? \
               OR description LIKE ? ORDER BY num ASC', (name, description,))
    for row in c:
        result = {'index':row[0], 'name':row[1], 'desc':row[2]}
        images['results'].append(result)
    db.close()
    return images

def generate_thumbnail(data):
    p = ImageFile.Parser()
    img = None
    try:
        p.feed(data)
        img = p.close()
    except IOError:
        print "Cannot generate image thumbnail"

    if img == None:
        dirname = os.path.join(os.path.dirname(__file__),"")
        thumbnail_path = os.path.join(dirname, DefaultThumbnail)
        return open(thumbnail_path, 'rb').read()
    else:
        fp = StringIO()
        img.thumbnail(ThumbnailSize, Image.ANTIALIAS)
        img.save(fp, format="PNG")
        fp.seek(0)
        return fp.read()

def get_image_count():
    db = sqlite3.connect('images.sqlite')
    c = db.cursor()
    c.execute('SELECT COUNT(*) FROM image_store')
    imageCount = c.fetchone()
    return imageCount[0]
