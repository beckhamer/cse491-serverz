import random
import socket
import time
import urlparse
from mimetools import Message
from StringIO import StringIO
import cgi
import app

import quixote
from quixote.demo import create_publisher
from quixote.demo.mini_demo import create_publisher
from quixote.demo.altdemo import create_publisher


_the_app = None
def make_app():
    global _the_app
    if _the_app is None:
        p = create_publisher()
        _the_app = quixote.get_wsgi_app()
    return _the_app




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
    environ['SCRIPT_NAME'] = ''
    environ['wsgi.input'] = StringIO(content)

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

    application = make_app()
    response_html = application(environ, start_response)
#    conn.send(response_html)
    for html in response_html:
        conn.send(html)
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
