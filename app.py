from urlparse import urlparse, parse_qs
import jinja2
import os
import cgi
from StringIO import StringIO
from wsgiref.simple_server import make_server

def path_render(path, query):
    loader = jinja2.FileSystemLoader('./templates')
    env = jinja2.Environment(loader=loader)
    template = env.get_template(path)
    x = template.render(query).encode('latin-1', 'replace')
    return str(x)

def simple_app(environ, start_response):

    method = environ['REQUEST_METHOD']
    path = environ['PATH_INFO']
    query = ''

    html_pages = {'/'                 :     'index.html',            \
                  '/content'          :     'content.html',          \
                  '/file'             :     'file.html',             \
                  '/image'            :     'image.html',            \
                  '/form'             :     'get_form.html',         \
                  '/form_default'     :     'form_default.html',     \
                  '/form_multipart'   :     'form_multipart.html',   \
                  '/submit'           :     'submit.html'            }

    if path in html_pages:
        start_response('200 OK', [('Content-type', 'text/html')])
        if path == '/submit':
            if method == 'GET':
                query = parse_qs(environ['QUERY_STRING'])
                query = dict(firstname=query['firstname'][0], lastname=query['lastname'][0])
            else:
                headers = {}
                headers['content-type'] = environ['CONTENT_TYPE']
                headers['content-length'] = environ['CONTENT_LENGTH']
                fs = cgi.FieldStorage(fp=environ['wsgi.input'], headers=headers, environ=environ)
                query = dict(firstname=fs['firstname'].value, lastname=fs['lastname'].value)
        return path_render(html_pages[path], query)

    else:
        start_response('404 Not Found', [('Content-type', 'text/html')])
        return path_render('error.html', query)

def make_app():
    return simple_app
