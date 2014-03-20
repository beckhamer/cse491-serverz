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
        

def test_handle_connection_index():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n'

    server.handle_connection(conn)

    assert conn.sent.startswith(expected_return), 'Got: %s' % (repr(conn.sent),)


def test_handle_connection_file():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/plain\r\n\r\n'

    server.handle_connection(conn)

    assert conn.sent.startswith(expected_return), 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n'

    server.handle_connection(conn)

    assert conn.sent.startswith(expected_return), 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_image():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: image/jpeg\r\n\r\n'

    server.handle_connection(conn)

    assert conn.sent.startswith(expected_return), 'Got: %s' % (repr(conn.sent),)                             

def test_handle_connection_form():
    conn = FakeConnection("GET /form HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n'

    server.handle_connection(conn)

    assert conn.sent.startswith(expected_return), 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_submit_GET():
    firstname = "John"
    lastname = "Smith"
    conn = FakeConnection("GET /submit?firstname=%s"%(firstname) + \
                          "&lastname=%s HTTP/1.0\r\n\r\n"%(lastname) )
                    
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n'

    server.handle_connection(conn)

    assert conn.sent.startswith(expected_return), 'Got: %s' % (repr(conn.sent),)
                          


def test_handle_connection_GET_404():
    conn = FakeConnection("GET /404 HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 404 Not Found'
    
    server.handle_connection(conn)

    assert conn.sent.startswith(expected_return), 'Got: %s' % (repr(conn.sent),)


def test_handle_connection_submit_POST_urlencoded():
    firstname = "Joe"
    lastname = "Schmoe"
    urlencoded = "firstname=%s&lastname=%s\r\n" % (firstname,lastname)
    conn = FakeConnection("POST /submit HTTP/1.0\r\n"+ \
                          "Content-Type: application/x-www-form-urlencoded \r\n" + \
                          "Content-Length: 29\r\n\r\n" + \
                          "firstname=%s&lastname=%s\r\n"%(firstname,lastname) )
                          
                          
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                          'Content-type: text/html\r\n\r\n'
    
    server.handle_connection(conn)

    assert (conn.sent.startswith(expected_return) and conn.sent.find('Hello Joe Schmoe') ), 'Got: %s' % (repr(conn.sent),)
    

def test_handle_connection_POST_404():
    conn = FakeConnection("POST /404 HTTP/1.0\r\n" + \
                          "Content-Type: application/x-www-form-urlencoded \r\n"+\
                          "Content-Length: 0\r\n\r\n")
    expected_return = 'HTTP/1.0 404 Not Found\r\n'
    
    server.handle_connection(conn)

    assert conn.sent.startswith(expected_return), 'Got: %s' % (repr(conn.sent),)

