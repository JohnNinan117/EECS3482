import struct

from dh import create_dh_key, calculate_dh_secret
from .xor import XOR

from enum import Enum

# Add messages
class Message(bytes, Enum):
     LIST  = bytes("LIST", "ascii")
     AUTH =  bytes("AUTH", "ascii")
     ECHO  = bytes("ECHO", "ascii")
     ERROR = bytes("ERROR", "ascii")
     CHAT = bytes("CHAT", "ascii")
     ACK    = bytes("OK", "ascii")
     CHAT_SESSION = bytes("PORT", "ascii")
     FILE = bytes("FILE", "ascii")
     FILE_TRANSFER = bytes("TRANSFER", "ascii")

class StealthConn(object):
    def __init__(self, conn,
                 client=False,
                 server=False,
                 user=None,
                 verbose=False):
        self.conn = conn
        self.cipher = None
        self.client = client
        self.server = server
        self.verbose = verbose
        self.user = user
        self.cipher= self.generate_secret()

    def generate_secret(self):
        # Perform the initial connection handshake for agreeing on a shared secret

        ### TODO: Your code here!
        
        # This can be broken into code run just on the server or just on the clientasdsad
        if self.server or self.client:
            my_public_key, my_private_key = create_dh_key()
            # Send them our public key
            self.send(bytes(str(my_public_key), "ascii"))
            # Receive their public key
            their_public_key = int(self.recv())
            # Obtain our shared secret
            shared_hash = calculate_dh_secret(their_public_key,
                                              my_private_key)

            self._secret = shared_hash
            if self.verbose:
                print("Shared hash: {}".format(shared_hash.encode("utf-8").hex()))

            # Default XOR algorithm can only take a key of length 32
            self.cipher = XOR.new(shared_hash[:4].encode("utf-8"))


    def send(self, data):
        if self.cipher:
            encrypted_data = self.cipher.encrypt(data)
            if self.verbose:
                print("Original data: {}".format(data))
                print("Encrypted data: {}".format(repr(encrypted_data)))
                print("Sending packet of length {}".format(len(encrypted_data)))
        else:
            encrypted_data = data

        # Encode the data's length into an unsigned two byte int ('H')
        pkt_len = struct.pack('H', len(encrypted_data))
        self.conn.sendall(pkt_len)
        self.conn.sendall(encrypted_data)

        #for testing
        #print("Sending to ", self.conn)
        return (struct.pack('H', len(encrypted_data)), encrypted_data)

    def recv(self):
        # Decode the data's length from an unsigned two byte int ('H')
        pkt_len_packed = self.conn.recv(struct.calcsize('H'))
        unpacked_contents = struct.unpack('H', pkt_len_packed)
        pkt_len = unpacked_contents[0]

        encrypted_data = self.conn.recv(pkt_len)
        if self.cipher:
            data = self.cipher.decrypt(encrypted_data)
            if self.verbose:
                print("Receiving packet of length {}".format(pkt_len))
                print("Encrypted data: {}".format(repr(encrypted_data)))
                print("Original data: {}".format(data))
        else:
            data = encrypted_data

        return data

    def close(self):
        self.conn.close()
