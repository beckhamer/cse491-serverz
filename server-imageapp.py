#!/usr/bin/env python
import random
import socket
import time
from urlparse import urlparse, parse_qs

## for the new POST request handling
from StringIO import StringIO
import cgi

## for the templates
import jinja2
import os

## for the wsgi app
# import app

## to run imageapp
import quixote
import imageapp

imageapp.setup()
p = imageapp.create_publisher()

def make_app():
    return quixote.get_wsgi_app()


##
## HANDLE CONNECTION DEFINITION
##
def handle_connection(conn):
    
    # Start reading in data from the connection
    read = conn.recv(1)
    while read[-4:] != '\r\n\r\n':
	read += conn.recv(1)

    if read[-4:] == '\r\n\r\n':
	print "READ IS DONE!"

    # Parse headers
    request, data = read.split('\r\n',1)
    print read

    headers = {}
    for line in data.split('\r\n')[:-2]:
	k, v = line.split(': ',1)
	headers[k.lower()] = v
    
    # parse path and query string as urlparse object
    # parsed_url[2] = path, parsed_url[4] = query string
    parsed_url = urlparse(request.split(' ', )[1])
    
    #initialize environ dictionary
    environ = {}
    
    environ['PATH_INFO'] = parsed_url[2]
    environ['QUERY_STRING'] = parsed_url[4]
    # temporary 'SCRIPT_NAME' entry
    environ['SCRIPT_NAME'] = ''
    # temporary 'SERVER_NAME' entry for arctic
    environ['SERVER_NAME'] = 'arctic.cse.msu.edu'
    
    # Handle reading of POST data
    content = ''
    if request.startswith('POST '):
	environ['REQUEST_METHOD'] = 'POST'
	environ['CONTENT_LENGTH'] = headers['content-length']
	environ['CONTENT_TYPE'] = headers['content-type']
	# read the remaining data from http request to construct wsgi.input
	while len(content) < int(headers['content-length']):
	    content += conn.recv(1)
    
    else:
	environ['REQUEST_METHOD'] = 'GET'
	environ['CONTENT_LENGTH'] = 0
    
    #form = cgi.FieldStorage(fp=StringIO(content), headers=headers, environ=environ)
   
    #environ['wsgi.input'] = cgi.FieldStorage(fp=StringIO(content), 
					      #headers = headers,
					      #environ = {'REQUEST_METHOD':'POST'} )
    environ['wsgi.input'] = StringIO(content)
    print 'wsgi.input made!'
    
    
    def start_response(status, response_headers):
	conn.send('HTTP/1.0 %s\r\n' % status)
	for header in response_headers:
	    conn.send('%s: %s\r\n' % header)
	conn.send('\r\n')

    # make the app	
    application = make_app()
    
    response_html = application(environ, start_response)
    for html in response_html:
        conn.send(html)
    print 'conn sent!'
    
    # close the connection
    conn.close()
    print 'conn closed!'





##
## MAIN FUNCTION DEFINITION
##

def main():
    s = socket.socket()         # Create a socket object
    host = socket.getfqdn()     # Get local machine name
    port = random.randint(8000, 9999)
    s.bind((host, port))        # Bind to the port
    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)
    s.listen(5)                 # Now wait for client connection.
    print 'Entering infinite loop; hit CTRL-C to exit'
    
    while True:

        # Ctrl+C KeyboardInterrupt error handler
        try:
            # Establish connection with client.
            c, (client_host, client_port) = s.accept()
            print 'Got connection from', client_host, client_port
            # handle connection to serve page
            handle_connection(c)

            
        except (KeyboardInterrupt):
            print "\r\nEnding server.py ...\r\n"
            exit(0)



##
## RUN MAIN
##

if __name__ == '__main__':
    main()

