## for parsing path and query string
from urlparse import urlparse, parse_qs

## for fieldstorage
from StringIO import StringIO
import cgi

## for the templates
import jinja2
import os



def simple_app(environ, start_response):
  
    # corrospond requests to .html files
    response = {
		'/'		: 'index.html',		\
		'/content'	: 'content.html',	\
		'/file'		: 'file.html',		\
		'/image'	: 'image.html',		\
		'/form'		: 'form.html',		\
		'/submit'	: 'submit.html',	\
		}
    
    # setup and run jinja2 templates
    loader = jinja2.FileSystemLoader('./templates')
    jinja2_environment = jinja2.Environment(loader=loader)
    
    
    # if any values are stored in the URL, this will get them
    values = parse_qs(environ['QUERY_STRING'])
    # initialize empty dictionary for POST requests that can be updated
    # with the contents of the awful cgi thing
    new_values = {}
    
    # create field storage object
    WSGIinput = cgi.FieldStorage(fp=environ['wsgi.input'], 
		 headers = environ,
		 environ = {'REQUEST_METHOD':'POST'} )
		      
    if environ['REQUEST_METHOD'] is 'POST':
      
	print "WSGIinput.keys()"
	print WSGIinput.keys()
	
	for key in WSGIinput.keys():
	    new_values[key] = WSGIinput[key].value
	    print "%s = %s \r\n" % (key, new_values[key])
	
	values.update(new_values)
	print 'values updated!' 
    
    
    # Try to connect to requested page
    if environ['PATH_INFO'] in response:
	response_status =	'200 OK'
	template = jinja2_environment.get_template(response[environ['PATH_INFO']])
    else:
	values['page'] = environ['PATH_INFO']
	response_status = '404 Not Found'
	template = jinja2_environment.get_template('404.html')
    
    # initialize return data
    data = []
    # set response_headers depending on the page content type
    if environ['PATH_INFO'] == '/image':
      response_headers = [('Content-type', 'image/jpeg')]
      # return image
      data.append(open_file('image.jpg') )
      
    elif environ['PATH_INFO'] == '/file':
      response_headers = [('Content-type', 'text/plain')]
      # return text file
      data.append(open_file('file.txt') )
      
    else:
      response_headers = [('Content-type', 'text/html')]
      # load template depending on the PATH_INFO
      # using jinja2's render to get the return string
      response_html = template.render(values).encode('latin-1', 'replace')
      data.append(response_html)
    
    print 'tried '+ environ['PATH_INFO']
    
    
    # start_response before building from template
    # does the app.send() for the status and headers
    start_response(response_status, response_headers)
    
    
    
    # return a list (actually a generator) titled data
    # which will be sent in the handle connection function
    return data
    
def open_file(file_name):
  '''Takes string of file name, returns open().read() as object'''
  file_obj = open(file_name, "rb")
  data = file_obj.read();
  file_obj.close()
  return data
    
# still needed?
def make_app():
    return simple_app
    
    