import random
import socket
import time
import urlparse
from mimetools import Message
from StringIO import StringIO
import cgi
import app
from wsgiref.validate import validator
import imageapp

imageapp.setup()
p = imageapp.create_publisher()

def make_app():
    return quixote.get_wsgi_app()

def handle_connection(conn):
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

    content = ''
    if request_method == 'POST':
        while len(content) < int(headers['Content-Length']):
            content += conn.recv(1)
        environ['CONTENT_TYPE'] = headers['Content-Type']
        environ['CONTENT_LENGTH'] = headers['Content-Length']
        environ['wsgi.input'] = cgi.FieldStorage(fp=StringIO(content), headers=headers.dict, environ=environ)
        
    def start_response(status, response_headers):
        conn.send('HTTP/1.0 ')
        conn.send(status)
        conn.send('\r\n')
        for pair in response_headers:
            key, header = pair
            conn.send(key + ': ' + header + '\r\n')
        conn.send('\r\n')

    application = make_app()
    validator_app = validator(application)
    response_html = application(environ, start_response)
    for data in response_html:
        conn.send(data)
    conn.close()

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

        handle_connection(c)

if __name__ == '__main__':
   main()
