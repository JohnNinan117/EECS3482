'''
    *  Full Name: John Ninan
    *  Course:EECS 3482 A
    *  Description:  Chat client.
    *
'''
import getopt
import socket
import sys
import threading
import time

from lib.comms import Message, StealthConn
from lib.files import recv_file


class Chat():
    def __init__(self, with_user=None):
        self._with_user = with_user
        self._conn = None
        self._sconn = None
        self._address = None
        self._port = None
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._s.bind(("localhost", 0))
        self._s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._s.listen(5)

        self._port = self._s.getsockname()[1]

    def get_connection_port(self):
        return self._port

    def get_session(self):
        return self._sconn

    def chat_thread(self):
        try:

            print("Chat session is on port %d" % self._port)
            print("Waiting for a connection...")
            self._conn, self._address = self._s.accept()
            print("Accepted a connection from %s..." % (self._address,))

            # Start a new thread per connection
            # We don't need to specify it's a daemon thread as daemon status is inherited
            threading.Thread(target=self.accept_connection).start()
                                #kwargs={ 'conn': self._conn}).start()
            time.sleep(2)
        except socket.error as e:
            print("Port %d not available" % self._port, e)
            exit()

    def accept_connection(self):
        try:
            self._sconn = StealthConn(self._conn, server=True)
            # The sender is either going to chat to us or send a file
            while True:
                try:
                    msg = self._sconn.recv()
                    if msg == Message.FILE_TRANSFER:
                        print("Ready to receive files")
                        recv_file(self._sconn)
                    else:
                        print(self._with_user+">"+msg.decode("utf-8"))
                except: #not a chat message
                     None
                time.sleep(2)
        except socket.error:
            print("Connection closed unexpectedly", socket.error)

    def start_session(self):
        # Start a new thread to accept a chat session connection
        thr = threading.Thread(target=self.chat_thread())
        # Daemon threads exit when the main program exits
        # This means the server will shut down automatically when we quit
        thr.setDaemon(True)
        thr.start()
