import random
import socket
import time
import urlparse
from mimetools import Message
from StringIO import StringIO
import cgi
from app import make_app
from wsgiref.validate import validator
import quixote
from quixote.demo.altdemo import create_publisher
import imageapp
import argparse
from chat.apps import ChatApp
from quotes.apps import QuotesApp

def handle_connection(conn, port, app):
    message = conn.recv(1)
    while message[-4:] != '\r\n\r\n':
        message += conn.recv(1)

    request, headers = message.split('\r\n',1)
    headers = Message(StringIO(headers))

    request_method = request.split()[0]
    request_url = request.split()[1]

    parsed_url = urlparse.urlparse(request_url)
    request_path = parsed_url.path

    environ = {}
    environ['REQUEST_METHOD'] = request_method
    environ['PATH_INFO'] = request_path
    environ['QUERY_STRING'] = parsed_url.query
    environ['CONTENT_TYPE'] = 'text/html'
    environ['CONTENT_LENGTH'] = 0
    environ['SCRIPT_NAME'] = ''
    environ['SERVER_NAME'] = socket.getfqdn()
    environ['SERVER_PORT'] = str(port)
    environ['wsgi.version'] = (1, 0)
    environ['wsgi.multithread'] = False
    environ['wsgi.multiprocess'] = False
    environ['wsgi.run_once'] = False
    environ['wsgi.url_scheme'] = 'http'
    environ['HTTP_COOKIE'] = headers['cookie'] if 'cookie' in headers.keys() else ''

    content = ''
    if request_method == 'POST':
        while len(content) < int(headers['Content-Length']):
            content += conn.recv(1)
        environ['CONTENT_TYPE'] = headers['Content-Type']
        environ['CONTENT_LENGTH'] = headers['Content-Length']

    environ['wsgi.input'] = StringIO(content)
        
    def start_response(status, response_headers):
        conn.send('HTTP/1.0 ')
        conn.send(status)
        conn.send('\r\n')
        for pair in response_headers:
            key, header = pair
            conn.send(key + ': ' + header + '\r\n')
        conn.send('\r\n')

    validator_app = validator(app)
    response_html = app(environ, start_response)
    for data in response_html:
        conn.send(data)
    conn.close()

def choose_app(app):
    if app == 'altdemo':
        p = create_publisher()
        return quixote.get_wsgi_app()
    elif app == 'image':
        imageapp.setup()
        p = imageapp.create_publisher()
        return quixote.get_wsgi_app() 
    elif app == 'myapp':
        return make_app()
    elif app == 'quotes': 
        return QuotesApp('./quotes/quotes.txt', './quotes/html')
    elif app == 'chat':
        return ChatApp('./chat/html')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-A', '--app', help='choose a app to run (image,altdemo,myapp)', default='myapp')
    parser.add_argument('-p', '--port', type=int, help='choose a port (default is random)', default=random.randint(8000,9999))
    args = parser.parse_args()
    app = choose_app(args.app)

    s = socket.socket()         # Create a socket object
    host = socket.getfqdn() # Get local machine name
    port = args.port 
    s.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.


    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port

        handle_connection(c, port, app)

if __name__ == '__main__':
   main()
