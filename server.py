#!/usr/bin/env python
import random
import socket
import time
import urlparse
import cgi
import cgitb
import jinja2
from mimetools import Message
from StringIO import StringIO

ok_response_line = 'HTTP/1.0 200 OK\r\n'
error_response_line = 'HTTP/1.0 404 Not Found\r\n'
header_line = 'Content-type: text/html\r\n\r\n'

loader = jinja2.FileSystemLoader('./templates')
env = jinja2.Environment(loader=loader)

def main():
    s = socket.socket()         # Create a socket object
    host = socket.getfqdn() # Get local machine name
    port = random.randint(8000, 9999)
    s.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port
        handle_connection(c);

def handle_connection(conn):
    message = conn.recv(1)
    while message[-4:] != '\r\n\r\n':
        message += conn.recv(1)

    request, headers= message.split('\r\n',1)
    headers = Message(StringIO(headers))

    request_method = request.split()[0]
    request_url = request.split()[1]

    parsed_url = urlparse.urlparse(request_url)
    request_path = parsed_url.path

    content = ''
    query = {}
    if request_method == 'POST':
        while len(content) < int(headers['content-length']):
            content += conn.recv(1)
        environ = {}
        environ['REQUEST_METHOD'] = 'POST'
        form = cgi.FieldStorage(fp=StringIO(content), headers=headers.dict, environ=environ)
        for key in form.keys():
            query[key] = form[key].value
    else:
        query = urlparse.parse_qs(parsed_url.query)
        if query != {}:
            query = dict(firstname=query['firstname'][0], lastname=query['lastname'][0])

    html_pages = {'/'                 :     'index.html',            \
                  '/content'          :     'content.html',          \
                  '/file'             :     'file.html',             \
                  '/image'            :     'image.html',            \
                  '/form'             :     'get_form.html',         \
                  '/form_default'     :     'form_default.html',     \
                  '/form_multipart'   :     'form_multipart.html',   \
                  '/submit'           :     'submit.html'            }

    if request_path in html_pages:
        conn.send(ok_response_line)
        conn.send(header_line)
        template = env.get_template(html_pages[request_path])
        conn.send(template.render(query))
    else:
        conn.send(error_response_line)
        conn.send(header_line)
        template = env.get_template('error.html')
        conn.send(template.render())

    conn.close()

if __name__ == '__main__':
    main()

