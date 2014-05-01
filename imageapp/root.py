import quixote
from quixote.directory import Directory, export, subdir

from . import html, image

class RootDirectory(Directory):
    _q_exports = []

    @export(name='')                    # this makes it public.
    def index(self):
        number = image.get_image_count()-1
        img = image.get_image(number)
        comments = image.get_comments(number)
        return html.render('index.html', {'name' : img[2], 'description' : img[3], 'comments' : comments, 'id' : number})

    @export(name='upload')    
    def upload(self):
        return html.render('upload.html')

    @export(name='upload_receive')
    def upload_receive(self):
        request = quixote.get_request()
        print request.form.keys()
        the_file = request.form['file']
        name = request.form['name']
        description = request.form['description']
        fileFormat = the_file.base_filename.split('.')[1].lower()
        if fileFormat in ['tiff', 'tif']:
        	fileFormat = 'image/tiff'
        elif fileFormat in ['jpeg', 'jpg']:
        	fileFormat = 'image/jpg'
        elif fileFormat in ['png']:
                fileFormat = 'image/png'
			
        print 'received file of format: ' + fileFormat
        print dir(the_file)
        print 'received file with name:', the_file.base_filename
        data = the_file.read(int(1e9))
        image.add_image(data, fileFormat, name, description)
        return quixote.redirect('./')

    @export(name='image')
    def image(self):
        request = quixote.get_request()
        if 'id' in request.form.keys():
            try:
                number = int(request.form['id'])
            except ValueError:
                print 'not a valid number!'
                number = image.get_image_count()-1
        else:
            number = image.get_image_count()-1
        img = image.get_image(number)
        comments = image.get_comments(number)
        return html.render('image.html', {'name' : img[2], 'description' : img[3], 'comments' : comments, 'id': number})

    @export(name='image_raw')
    def image_raw(self):
        response = quixote.get_response()
        request = quixote.get_request()

        if 'id' in request.form.keys():
            try:
                number = int(request.form['id'])
            except ValueError:
                print 'input number is not a valid number!'
                number = image.get_image_count() - 1
            if number not in range(0, image.get_image_count()):
                number = image.get_image_count() - 1
        else:
            number = image.get_image_count() - 1
        img = image.get_image(number)       
        response.set_content_type(img[1])     
        return img[0]

    @export(name='list')
    def list(self):
    	results = image.get_all_images()
        return html.render('list.html', results )

    @export(name='search')
    def search(self):
    	return html.render('search.html')
    
    @export(name='result')
    def result(self):
    	response = quixote.get_request()   	
    	name = response.form['name']
        description = response.form['description']		
    	results = image.search(name, description)
    	return html.render('result.html', results)

    @export(name='thumbnails')
    def thumbnails(self):
        results = image.get_all_images()
        return html.render('thumbnails.html', results )
    
    @export(name='get_thumbnail')
    def get_thumb(self):
        request = quixote.get_request()
        response = quixote.get_response()        
        number = int(request.form['id'])
        img = image.get_image(number)
        thumb = image.generate_thumbnail(img[0])
        response.set_content_type('image/png')        
        return thumb

    @export(name='add_comment')
    def add_comment(self):
        response = quixote.get_response()
        request = quixote.get_request()
        number = request.form['id']
        comment = request.form['comment']
        image.add_comment(number, comment)
        return quixote.redirect('./image?id='+str(number))

    @export(name='bkgrnd.gif')
    def body_jpg(self):
        data = html.get_image('bkgrnd.gif')
        return data

    @export(name='grapes.jpg')
    def content_jpg(self):
        data = html.get_image('grapes.jpg')
        return data

    @export(name='quote.gif')
    def footer_gif(self):
        data = html.get_image('quote.gif')
        return data
