'''
    *  Full Name: John Ninan
    *  Course:EECS 3482 A
    *  Description:  Server program. Accepts connections  from client programs
    *
'''
from base64 import b64encode
import socket
import time
import threading
import sys, getopt
import traceback

import pyfiglet

from lib.comms import StealthConn
from lib.comms import Message
from Crypto.Hash import SHA256 
from Crypto.Protocol.KDF import bcrypt_check

class Server:
    def __init__(self, server_port):
        self._port = server_port
        # active users
        # TODO(JN): make password stronger
        self._users={b"user1":b"$2a$12$s2cBZLaGq.lAviOC4fIrle9zNjHa.1mYwcJq6TvNMlpeLKZXD3Qde", # Actual Password: 25Viking
                    b"user2":b"$2a$12$0Ibf/kJn3Kp8Jgx9PQXctuRlIQhEGgOCnVmmNiZnVIUEIX6kGtCDm", # Actual Password: 35Viking
                    b'user3':b'$2a$12$1EGn7t2.qGp9IAU9jsDbauwTtujntZbFOURJvW5odwe.yNl.8kzre'} # Actual Password: 1393Williams

        self._users_connections={}

    def file_transfer(self, sconn):
        try:
            user = sconn.recv()
            print(user)
            user_conn = self._users_connections[user]
            if user != sconn.user:
                user_conn.send(Message.FILE)
                user_conn.send(sconn.user)
            else:
                print("Attempting to send a file to themselves!")
        except:
            sconn.send(Message.ERROR)
            print("User is not online'")


    def chat_session(self, sconn):
            try:
                user = sconn.recv()
                user_conn=self._users_connections[user]
                #chat_msg = sconn.recv()
                if user != sconn.user:
                    user_conn.send(Message.CHAT)
                    user_conn.send(sconn.user)

                else:
                    print("Attempting to chat with themselves")

            except KeyError:
                sconn.send(Message.ERROR)
                #traceback.print_exc()
                print("User is not online")



    def echo_server(self,sconn):
        data = sconn.recv()


    def get_users_list(self,current_user):
        online_users = list(self._users.keys())
        online_users.remove(current_user)
        if len(online_users) > 0:
            return b" ".join(online_users)
        else:
            return b'None'


    def auth(self,sconn):
        user = sconn.recv()

        if sconn.verbose:
            print("User:", user)

        pwd = sconn.recv()
        b64pwd = b64encode(SHA256.new(pwd).digest())
        try:
            bcrypt_check(b64pwd,self._users.get(user.lower()))
            if sconn.verbose:
                print("User authenticated")
            sconn.user = user
            sconn.send(Message.ACK)
            if sconn.verbose:
                print("Sending user list")
            sconn.send(Message.LIST)
            sconn.send(self.get_users_list(user))
            try:
                self._users_connections[user] = sconn
            except KeyError:
                self._users_connections.update({user:sconn})
            for u, c in self._users_connections.items():
                print(u, ":", c.conn.getsockname())

        except ValueError:
            sconn.send(Message.ERROR)

        return None

    def accept_connection(self,sconn):
            #sconn = StealthConn(conn, server=True, verbose = True)
            # The sender is either going to chat to us or send a file
            while True:
                cmd = sconn.recv()
                print("Received", cmd)
                if cmd == Message.ECHO:
                    data = sconn.recv()
                    if sconn.verbose:
                        print("ECHOING>", data)
                    sconn.send(Message.ECHO)
                    sconn.send(data)
                    if data == b'X' or data == b'exit':
                        print("Closing connection...")
                        sconn.close()

                elif cmd == Message.CHAT:
                    if sconn.verbose:
                        print("Establishing chat session")
                    self.chat_session(sconn)

                elif  cmd == Message.FILE:
                   if sconn.verbose:
                       print("Establishing filetransfer")
                   self.file_transfer(sconn)

                elif cmd == Message.CHAT_SESSION or\
                    cmd == Message.FILE_TRANSFER:
                    chat_user = sconn.recv()
                    chat_user_port = sconn.recv()
                    print(chat_user, chat_user_port)
                    user_conn=self._users_connections[chat_user]
                    user_conn.send(cmd) # forward the original cmd
                    user_conn.send(chat_user_port)

                elif cmd == Message.AUTH:
                    if sconn.verbose:
                        print("Authticating user")
                    self.auth(sconn)

                elif cmd == Message.LIST:
                    if sconn.verbose:
                        print("Sending user list")
                        print(self.get_users_list(sconn.user))
                    sconn.send(Message.LIST)
                    #sending the users
                    sconn.send(self.get_users_list(sconn.user))



    def server_thread(self,port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind(("localhost", port))
            print("Listening on port %d" % port)

            s.listen(5)

            while True:
                print("Waiting for connection...")
                conn, address = s.accept()
                print("Accepted a connection from %s..." % (address,))

                sconn = StealthConn(conn, server=True, verbose = True)
                # Start a new thread per connection
                # We don't need to specify it's a daemon thread as daemon status is inherited
                threading.Thread(target=self.accept_connection, kwargs={ 'sconn': sconn}).start()
                                 #args=(conn,)).start()
        except socket.error:
            # Someone is already using that port -- let's go up one
            print("Port %d not available" % port)
            exit()
            ## server_port += 1


    def start(self):
        # Start a new thread to accept client connection
        thr = threading.Thread(target=self.server_thread(self._port))
        # Daemon threads exit when the main program exits
        # This means the server will shut down automatically when we quit
        thr.setDaemon(True)
        thr.start()
        # Wait for a small amount of time so that the output
        # doesn't play around with our "command prompt"
        time.sleep(0.3)

def main(argv):
    server_port=1337
    try:
        opts, args = getopt.getopt(argv,"hp:",["port="])
    except getopt.GetoptError:
        print('server.py -port <port>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('server.py -port <port>')
            sys.exit()
        elif opt in ("-p", "--port"):
            if arg:
                server_port = int(arg)

    welcome_msg= pyfiglet.figlet_format("Welcome to EECS 3482 Net", font = "digital" )
    print(welcome_msg)
    server = Server(server_port)
    server.start()
if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print("\nDone!")
