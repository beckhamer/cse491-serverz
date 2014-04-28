import quixote
from quixote.directory import Directory, export, subdir

from . import html, image

class RootDirectory(Directory):
    _q_exports = []

    @export(name='')                    # this makes it public.
    def index(self):
        return html.render('index.html')

    @export(name='upload')
    def upload(self):
        return html.render('upload.html')

    @export(name='upload_receive')
    def upload_receive(self):
        request = quixote.get_request()
        print request.form.keys()

        the_file = request.form['file']
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

        image.add_image(data)

        return quixote.redirect('./')

    @export(name='image')
    def image(self):
        return html.render('image.html')

    @export(name='image_raw')
    def image_raw(self):
        response = quixote.get_response()
        request = quixote.get_request()
        number = request.form['special']

        if(number == 'latest'):
            img = image.get_latest_image()
        else:
            img = image.get_image(int(number))
        response.set_content_type(img[1])     
        return img[0]
		
    @export(name='list')
    def image_list(self):
        return html.render('list.html', {'total' : len(image.images)})
