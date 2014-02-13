
from urlparse import urlparse, parse_qs
import jinja2
import os

def path_render(path, query):
    loader = jinja2.FileSystemLoader('./templates')
    env = jinja2.Environment(loader=loader)
    template = env.get_template(path)
    return template.render(query).encode('latin-1', 'replace')

def simple_app(environ, start_response):

    # handle different path
    path = {
		'/'			: 'index.html',		\
		'/content'		: 'content.html',	\
		'/file'			: 'file.html',		\
		'/image'		: 'image.html',		\
		'/get_form'		: 'get_form.html',	\
		'/form_default'		: 'form_default.html',	\
		'/form_multipart'	:'form_multipart.html',	\
		'/submit'		: 'submit.html',	\
		}
    
    method = environ['REQUEST_METHOD']
    path = environ['PATH_INFO']
    if method == 'GET':
	if path == '/':
	    start_response('200 OK', [('Content-type', 'text/html')])
	    return path_render('index.html', '')
	elif path == '/content':
	    start_response('200 OK', [('Content-type', 'text/html')])
	    return path_render('content.html', '')
	elif path == '/file':
	    start_response('200 OK', [('Content-type', 'text/html')])
	    return path_render('file.html', '')
	elif path == '/image':
	    start_response('200 OK', [('Content-type', 'text/html')])
	    return path_render('image.html', '')
	elif path == '/form':
	    start_response('200 OK', [('Content-type', 'text/html')])
	    return path_render('get_form.html', '')
	elif path == '/form_default':
	    start_response('200 OK', [('Content-type', 'text/html')])
	    return path_render('form_default.html', '')
	elif path == '/form_multipart':
	    start_response('200 OK', [('Content-type', 'text/html')])
	    return path_render('form_multipart.html', '')
	elif path == '/submit':
	    start_response('200 OK', [('Content-type', 'text/html')])
	    query = parse_qs(environ['QUERY_STRING'])
	    query = dict(firstname=query['firstname'][0], lastname=query['lastname'][0])
	    return path_render('submit.html', query)
	else:
            start_response('404 Not Found', [('Content-type', 'text/html')])
            return path_render('error.html', '')

    elif method == 'POST':
	if path == '/':
	    start_response('200 OK', [('Content-type', 'text/html')])
            return path_render('index.html', '')
	elif path == '/form_default':
            start_response('200 OK', [('Content-type', 'text/html')])
            return path_render('form_default.html', '')	   
	elif path == '/form_multipart':
            start_response('200 OK', [('Content-type', 'text/html')])
            return path_render('form_multipart.html', '')
	elif path == '/submit':
            query = dict(firstname=environ['wsgi.input']['firstname'].value, lastname=environ['wsgi.input']['lastname'].value)
	    start_response('200 OK', [('Content-type', 'text/html')])
            return path_render('submit.html', query)
	else:
            start_response('404 Not Found', [('Content-type', 'text/html')])
            return path_render('error.html', '')

def make_app():
    return simple_app
    
