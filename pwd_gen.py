from Crypto.Hash import SHA256 
from Crypto.Protocol.KDF import bcrypt

from base64 import b64encode

pwd = b"1393Williams"
b64pwd = b64encode(SHA256.new(pwd).digest())
bcrypt_hashed_password = bcrypt(b64pwd, 12)
print(pwd, bcrypt_hashed_password)