import server

class FakeConnection(object):
    """
    A fake connection class that mimics a real TCP socket for the purpose
    of testing socket I/O.
    """
    def __init__(self, to_recv):
        self.to_recv = to_recv
        self.sent = ""
        self.is_closed = False

    def recv(self, n):
        if n > len(self.to_recv):
            r = self.to_recv
            self.to_recv = ""
            return r
            
        r, self.to_recv = self.to_recv[:n], self.to_recv[n:]
        return r

    def send(self, s):
        self.sent += s

    def close(self):
        self.is_closed = True

# Test a basic GET call.

def test_handlen_index():
    conn = FakeConnection("GET / HTTP/1.0\r\n" + \
			  "host:arctic.cse.msu.edu:8000/ \r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n' + \
                      '<html><body>\n' + \
                      '<title>Index page</title>\n' + \
                      "This is beckhamer's index page.<br>\n" + \
                      "<a href='/content'>Content page</a><br>\n" + \
                      "<a href='/file'>File page</a><br>\n" + \
                      "<a href='/image'>Image page</a><br>\n" + \
                      "<a href='/form'>Get Form page</a><br>\n" + \
		      "<a href='/form_default'>Form page: application/x-www-form-urlencoded</a><br>\n" + \
		      "<a href='/form_multipart'>Form page: multipart/form-data</a><br>\n" + \
		      "<a href='/404'>Error page</a><br>\n"	+ \
                      '</body></html>' 
    
    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)
   
def test_handle_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n" + \
         		  "host:arctic.cse.msu.edu:8000/ \r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n' + \
                      '<html><body>\n' + \
                      '<title>Content page</title>\n' + \
                      "This is beckhamer's content page.<br>\n" + \
                      '</body></html>'                       

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_file():
    conn = FakeConnection("GET /file HTTP/1.0\r\n" + \
        		  "host:arctic.cse.msu.edu:8000/ \r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n' + \
                      '<html><body>\n' + \
                      '<title>File page</title>\n' + \
                      "This is beckhamer's file page.<br>\n" + \
                      '</body></html>' 

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_image():
    conn = FakeConnection("GET /image HTTP/1.0\r\n" + \
                          "host:arctic.cse.msu.edu:8000/ \r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n' + \
                      '<html><body>\n' + \
                      '<title>Image page</title>\n' + \
                      "This is beckhamer's image page.<br>\n" + \
                      '</body></html>' 

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_get_form():
    conn = FakeConnection("GET /form HTTP/1.0\r\n" + \
                          "host:arctic.cse.msu.edu:8000/ \r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n' + \
                      '<html><body>\n' + \
		      '<title>GET Form page</title>\n' + \
		      "<form action='/submit' method='GET'>\n" + \
		      "First name:<input type='text' name='firstname'>\n" + \
		      "Last name:<input type='text' name='lastname'>\n" + \
		      "<input type='submit' value='Submit'> </form>\n" + \
		      '</body></html>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_submit():
    conn = FakeConnection("GET /submit?firstname=Tao&lastname=Feng HTTP/1.0\r\n" + \
	                  "host:arctic.cse.msu.edu:8000/ \r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n' + \
                      '<html><body>' + \
                      "Hello Mr. Tao Feng." + \
                      '</body></html>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)
    
def test_handle_post_index():
    conn = FakeConnection("POST / HTTP/1.0\r\n" + \
		      "Content-Type: text/html\r\n" + \
		       "Content-Length: 0\r\n" + \
			  "host:arctic.cse.msu.edu:8000/ \r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n' + \
                      '<html><body>\n' + \
                      '<title>Index page</title>\n' + \
                      "This is beckhamer's index page.<br>\n" + \
                      "<a href='/content'>Content page</a><br>\n" + \
                      "<a href='/file'>File page</a><br>\n" + \
                      "<a href='/image'>Image page</a><br>\n" + \
                      "<a href='/form'>Get Form page</a><br>\n" + \
		      "<a href='/form_default'>Form page: application/x-www-form-urlencoded</a><br>\n" + \
		      "<a href='/form_multipart'>Form page: multipart/form-data</a><br>\n" + \
		      "<a href='/404'>Error page</a><br>\n"	+ \
                      '</body></html>' 

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_post_form_default():
    conn = FakeConnection("POST /form_default HTTP/1.0\r\n" + \
		      "Content-Type: text/html\r\n" + \
		      "Content-Length: 0\r\n" + \
			  "host:arctic.cse.msu.edu:8000/ \r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n' + \
                      '<html><body>\n' + \
                      '<title>Form page: application/x-www-form-urlencoded</title>\n' + \
                      "<form action='/submit' method='POST' enctype='application/x-www-form-urlencoded'>\n" + \
                      "First name:<input type='text' name='firstname'>\n" + \
                      "Last name:<input type='text' name='lastname'>\n" + \
                      "<input type='submit' value='Submit'> </form>\n" + \
                      '</body></html>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_post_form_multipart():
    conn = FakeConnection("POST /form_multipart HTTP/1.0\r\n" + \
                          "Content-Type: text/html\r\n"  + \
                          "Content-Length: 0\r\n" + \
			  "host:arctic.cse.msu.edu:8000/ \r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n' + \
                      '<html><body>\n' + \
                      '<title>Form page: multipart/form-data</title>\n' + \
                      "<form action='/submit' method='POST' enctype='multipart/form-data'>\n" + \
                      "First name:<input type='text' name='firstname'>\n" + \
                      "Last name:<input type='text' name='lastname'>\n" + \
                      "<input type='submit' value='Submit'> </form>\n" + \
                      '</body></html>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_post_submit_multipart():
    conn = FakeConnection("POST /submit HTTP/1.0\r\n" + \
			  "Content-Length: 183\r\n" + \
			  "Content-Type: multipart/form-data; boundary=b3f2eea10bf64ea89786c327b60a022a\r\n" + \
			  "Accept-Encoding: gzip, deflate, compress\r\n" + \
			  "Accept: */*\r\n" + \
			  "User-Agent: python-requests/0.14.2 CPython/2.7.3 Darwin/12.5.0\r\n\r\n" + \
			  "--b3f2eea10bf64ea89786c327b60a022a\r\n" + \
			  'Content-Disposition: form-data; name="firstname"\r\n' + \
			  'Content-Type: application/octet-stream\r\n\r\n' + \
			  "Tao\r\n" + \
                          "--b3f2eea10bf64ea89786c327b60a022a\r\n" + \
                          'Content-Disposition: form-data; name="lastname"\r\n' + \
                          "Content-Type: application/octet-stream\r\n\r\n" + \
                          "Feng\r\n" + \
			  "--b3f2eea10bf64ea89786c327b60a022a--\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n' + \
                      '<html><body>' + \
                      'Hello Mr. Tao Feng.' + \
                      '</body></html>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_post_submit_default():
    conn = FakeConnection("POST /submit HTTP/1.0\r\n" + \
                          "Content-Length: 27\r\n" + \
                          "Content-Type: application/x-www-form-urlencoded\r\n\r\n" + \
                          "firstname=Tao&lastname=Feng")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n' + \
                      '<html><body>' + \
                      'Hello Mr. Tao Feng.' + \
                      '</body></html>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_404():
    conn = FakeConnection("GET /404 HTTP/1.0\r\n" + \
			  "host:arctic.cse.msu.edu:8000/ \r\n\r\n")
    expected_return = 'HTTP/1.0 404 Not Found\r\n' + \
                      'Content-type: text/html\r\n\r\n' + \
                      '<html><body>\n' + \
                      '<title>Error page</title>\n' + \
                      "This is beckhamer's error page.<br>\n" + \
                      '</body></html>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)