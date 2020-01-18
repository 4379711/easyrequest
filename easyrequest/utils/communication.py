# -*- coding: utf-8 -*-

import socket


class ControlEngine:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = '127.0.0.1'
        self.port = 43797
        self.s.bind((self.host, self.port))

    def server(self):
        self.s.listen(5)
        while True:
            c, addr = self.s.accept()
            data = c.recv(1024)
            print(data.decode('utf-8'))
            c.close()

    def client(self):
        self.s.connect((self.host, self.port))
        self.s.send('exit xxx'.encode('utf-8'))
        self.s.close()
