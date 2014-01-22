#!/usr/bin/env python
import random
import socket
import time

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
    request_method =  message.splitlines()[0].split()[0]
    request_path = message.splitlines()[0].split()[1]
    print 'request method:'+request_method
    print 'request path:'+request_path

    # handle different types of HTML requests
    if request_method == 'GET':
        if request_path == '/':
            html_content = 'This is / page.'
        elif request_path == '/content':
	    html_content = 'This is /content page.'
	elif request_path == '/file':
	    html_content = 'This is /file page.'
        elif request_path == '/image':
	    html_content = 'This is /image page.'
	elif request_path == '/favicon.ico':
	    html_content = 'This is /favicon.ico page.'
    elif request_method == 'POST':
	    html_content = 'This is POST request html.'
	
    # send a response
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n')
    conn.send('<h1>Hello, world.</h1>')
    conn.send(html_content)
    conn.close()

if __name__ == '__main__':
    main()
