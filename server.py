import random
import socket
import time
import urlparse
from mimetools import Message
from StringIO import StringIO
import cgi
import app

def handle_connection(conn):
    receive = conn.recv(2000)
    request_headers, content= receive.split('\r\n\r\n',1)
    raw_request, raw_headers= request_headers.split('\r\n',1)
    headers = Message(StringIO(raw_headers))
    request_method = raw_request.split()[0]
    request_url = raw_request.split()[1]
    parsed_url = urlparse.urlparse(request_url)
    request_path = parsed_url.path

    environ = {}
    environ['REQUEST_METHOD'] = request_method
    environ['PATH_INFO'] = request_path
    environ['QUERY_STRING'] = parsed_url.query
    environ['CONTENT_TYPE'] = 'text/html'
    environ['CONTENT_LENGTH'] = 0

    if request_method == 'POST':
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

    response_html = app.simple_app(environ, start_response)
    conn.send(response_html)
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
