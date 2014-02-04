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

def test_handle_connection_index():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n' + \
                      '<html><body>' + \
                      '<h1>Hello, world.</h1>' + \
                      "This is beckhamer's page.<br>" + \
                      "<a href='/content'>Content page</a><br>" + \
                      "<a href='/file'>File page</a><br>" + \
                      "<a href='/image'>Image page</a><br>" + \
                      "<a href='/form'>Form page</a><br>" + \
                      '</html></body>' 
    
    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)
   
def test_handle_connection_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n' + \
                      '<html><body>' + \
                      '<h1>Content page</h1>' + \
                      "This is beckhamer's content page.<br>" + \
                      '</html></body>'                       

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_file():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n' + \
                      '<html><body>' + \
                      '<h1>File page</h1>' + \
                      "This is beckhamer's file page.<br>" + \
                      '</html></body>' 

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_image():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n' + \
                      '<html><body>' + \
                      '<h1>Image page</h1>' + \
                      "This is beckhamer's image page.<br>" + \
                      '</html></body>' 

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_form():
    conn = FakeConnection("GET /form HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n' + \
                      '<html><body>' + \
                      "<form action='/submit' method='GET\'>" + \
                      "First name:<input type='text' name='firstname'>" + \
                      "Last name:<input type='text' name='lastname'>" + \
                      "<input type='submit' value='Submit'> </form>" + \
                      '</html></body>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_GET_submit():
    conn = FakeConnection("GET /submit?firstname=Tao&lastname=Feng \r\n" + \
                          "HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n' + \
                      '<html><body>' + \
                      "Hello Mr. Tao Feng." + '</html></body>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)
    
def test_handle_connection_POST():
    conn = FakeConnection("POST / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n' + \
                      '<html><body>' + \
                      '<h1>Hello, world.</h1>' + \
                      "This is beckhamer's page.<br>" + \
                      "<a href='/content'>Content page</a><br>" + \
                      "<a href='/file'>File page</a><br>" + \
                      "<a href='/image'>Image page</a><br>" + \
                      "<a href='/form'>Form page</a><br>" + \
                      '</html></body>' 

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_POST_submit():
    conn = FakeConnection("POST /submit HTTP/1.0\r\n\r\n" + \
			  "firstname=Tao&lastname=Feng\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n' + \
                      '<html><body>' + \
                      'Hello Mr. Tao Feng.' + '</html></body>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

