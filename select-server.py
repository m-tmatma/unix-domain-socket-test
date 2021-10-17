#!/usr/bin/python3
import os
import sys
import socket
import select

class Server:
    def __init__(self, socket_path):
        self.socket_path = socket_path

    def process(self, r_ready, w_ready, x_ready):
        print("----------------------------------------------------------------")
        print("r_ready", r_ready)
        print("w_ready", w_ready)
        print("----------------------------------------------------------------")

        for s in r_ready:
            if s in self.listen_fds:
                conn, addr = self.socket.accept()
                conn.setblocking(False)
                self.read_fds.append(conn)
            else:
                data = s.recv(1024)
                if len(data) == 0:
                    print("close")
                    s.close()
                    self.read_fds.remove(s)
                    if s in self.write_fds:
                        self.write_fds.remove(s)
                    return
                print(data)
                self.write_fds.append(s)

        for s in w_ready:
            if s in self.write_fds:
                print("sending test")
                s.send("test".encode())
                self.write_fds.remove(s)


    def start(self):
        if os.path.exists(self.socket_path):
            os.remove(self.socket_path)

        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket.bind(self.socket_path)
        self.socket.listen(5)
        self.socket.setblocking(False)
        self.listen_fds = [self.socket]
        self.read_fds =  [self.socket]
        self.write_fds =  []
        while True:
            r_ready, w_ready, x_ready = select.select(self.read_fds, self.write_fds, [])
            self.process(r_ready, w_ready, x_ready)

def main():
    server = Server('/tmp/myapp.sock')
    server.start()

if __name__ == '__main__':
    main()
