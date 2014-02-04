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
    request_url = message.splitlines()[0].split()[1]
    print request_url
    parsed_url = urlparse.urlparse(request_url)
    print parsed_url
    request_path = parsed_url.path
    
    print 'request method:'+request_method
    print 'request path:'+request_path    
    
    # handle different types of HTML requests
    if request_method == 'GET':
        if request_path == '/':
	    handle_index(conn, parsed_url)
	elif request_path == '/content':
	    handle_content(conn, parsed_url)
	elif request_path == '/file':
	    handle_file(conn, parsed_url)
	elif request_path == '/image':
	    handle_image(conn, parsed_url)
	elif request_path == '/form':
	    handle_form(conn, parsed_url)
	elif request_path == '/submit':
	    handle_submit(conn, parsed_url)
    elif request_method == 'POST':
        content = message.splitlines()[-1]
        if request_path == '/':
	    handle_post_index(conn, content)
        elif request_path == '/submit':
            handle_post_submit(conn, content)
    conn.close()

def handle_index(conn, parsed_url):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n\r\n')
    conn.send('<html><body>')
    conn.send('<h1>Hello, world.</h1>')
    conn.send("This is beckhamer's page.<br>")
    conn.send("<a href='/content'>Content page</a><br>")
    conn.send("<a href='/file'>File page</a><br>")
    conn.send("<a href='/image'>Image page</a><br>")
    conn.send("<a href='/form'>Form page</a><br>")
    conn.send('</html></body>')

def handle_content(conn, parsed_url):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n\r\n')
    conn.send('<html><body>')
    conn.send('<h1>Content page</h1>')
    conn.send("This is beckhamer's content page.<br>")
    conn.send('</html></body>')

def handle_file(conn, parsed_url):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n\r\n')
    conn.send('<html><body>')
    conn.send('<h1>File page</h1>')
    conn.send("This is beckhamer's file page.<br>")
    conn.send('</html></body>')

def handle_image(conn, parsed_url):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n\r\n')
    conn.send('<html><body>')
    conn.send('<h1>Image page</h1>')
    conn.send("This is beckhamer's image page.<br>")
    conn.send('</html></body>')

def handle_form(conn, parsed_url):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n\r\n')
    conn.send('<html><body>')
    conn.send("<form action='/submit' method='GET'>")
    conn.send("First name:<input type='text' name='firstname'>")
    conn.send("Last name:<input type='text' name='lastname'>")
    conn.send("<input type='submit' value='Submit'> </form>")
    conn.send('</html></body>')

def handle_submit(conn, parsed_url):
    query = urlparse.parse_qs(parsed_url.query)
    print 'query:'+query['firstname'][0]+' '+query['lastname'][0]
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n\r\n')
    conn.send('<html><body>')
    conn.send('Hello Mr. ')
    conn.send(query['firstname'][0])
    conn.send(' ')
    conn.send(query['lastname'][0])
    conn.send('.')
    conn.send('</html></body>')

def handle_post_index(conn, content):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n\r\n')
    conn.send('<html><body>')
    conn.send('<h1>Hello, world.</h1>')
    conn.send("This is beckhamer's page.<br>")
    conn.send("<a href='/content'>Content page</a><br>")
    conn.send("<a href='/file'>File page</a><br>")
    conn.send("<a href='/image'>Image page</a><br>")
    conn.send("<a href='/form'>Form page</a><br>")
    conn.send('</html></body>')

def handle_post_submit(conn, content):
    query = urlparse.parse_qs(content)
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n\r\n')
    conn.send('<html><body>')
    conn.send('Hello Mr. ')
    conn.send(query['firstname'][0])
    conn.send(' ')
    conn.send(query['lastname'][0])
    conn.send('.')
    conn.send('</html></body>')

if __name__ == '__main__':
    main()
