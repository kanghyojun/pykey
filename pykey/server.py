import socket

class Server(object):
 
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def get_sock(self):
        try:
            self.s.bind((self.host, self.port))
        except socket.error:
            print "storage.server error :: Address already used"
            self.s.close()
        self.s.listen(2)
        return self.s
