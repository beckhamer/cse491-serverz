#!/usr/bin/env python
import random
import socket
import time
import urlparse
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
    # receive message
    message = conn.recv(1000)
    # print message
    request_method =  message.splitlines()[0].split()[0]
    local_path  = message.splitlines()[0].split()[1]
    host_url = "http://arctic.cse.msu.edu"
    request_url = host_url+local_path
    # print request_url
    parsed_url = urlparse.urlparse(request_url)
    print parsed_url
    request_path = parsed_url.path
    request_query = parsed_url.query

#     if local_path.find("?")>0:
#         request_path = local_path.split("?")[0]
#         request_data = local_path.split("?")[1]
#     else:
#         request_path = local_path

    print 'request method:'+request_method
    print 'request path:'+request_path    
    print 'request query:'+request_query
    # handle different types of HTML requests
    if request_method == 'GET':
        if request_path == '/':
            html_content = '<form action=\'/submit\' method=\'GET\'>' + \
			   'First name:<input type=\'text\' name=\'firstname\'>' + \
			   'Last name:<input type=\'text\' name=\'lastname\'>' + \
			   '<input type=\'submit\' value=\'Submit\'>' + \
			   '</form>'
	elif request_path == '/submit':
	    parsed_query = urlparse.parse_qs(request_query,True)
        
	    firstname = ''.join(parsed_query['firstname'])
# 	    firstname = request_data.split("&")[0].split("=")[1]
	    lastname = ''.join(parsed_query['lastname'])
# 	    lastname = request_data.split("&")[1].split("=")[1]
            html_content = 'Hello Mr %s %s.' % (firstname, lastname)	    
        elif request_path == '/content':
	    html_content = 'This is /content page.'
	elif request_path == '/file':
	    html_content = 'This is /file page.'
        elif request_path == '/image':
	    html_content = 'This is /image page.'
	elif request_path == '/favicon.ico':
	    html_content = 'This is /favicon.ico page.'
    elif request_method == 'POST':
	if request_path == '/':
	    html_content = 'This is POST request page.'
	elif request_path == '/submit':
	    html_content = 'Hello Mr Tao Feng.'
	
    # send a response
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n')
    conn.send('<h1>Hello, world.</h1>')
    conn.send(html_content)
    conn.close()

#def handle_form(conn):
#    message = conn.recv(1000)
#    request_method = message.splitlines()[0].split[0]
#    request_path =messgae.splitlines()[0].split()[1]
if __name__ == '__main__':
    main()
