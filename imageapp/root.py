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
        if fileFormat == 'tiff' or fileFormat == 'tif':
            fileFormat = 'tiff'
        elif fileFormat == 'jpeg' or fileFormat == 'jpg':
            fileFormat = 'jpg'
			
	print 'received file of format: ' + fileFormat
        print dir(the_file)
        print 'received file with name:', the_file.base_filename
        data = the_file.read(int(1e9))

        image.add_image(data)

        #return quixote.redirect('index.html') # was ./html
	return html.render('index.html')
        
    @export(name='image')
    def image(self):
        return html.render('image.html')

    @export(name='image_raw')
    def image_raw(self):
        response = quixote.get_response()
        img = image.get_latest_image()
        response.set_content_type('image/%s' % img[1])
        return img
