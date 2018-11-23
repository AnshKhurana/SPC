# AES 256 encryption/decryption using pycrypto library

import base64
import hashlib
from ast import literal_eval

from Crypto.Cipher import AES
from Crypto import Random

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

# password = input("Enter encryption password: ")


def encrypt(filename, key):
    private_key = hashlib.sha256(key.encode()).digest()
    print(private_key)
    raw= open(filename,'rb').read()
    print(raw)
    # print(type(raw))
    raw = pad(str(literal_eval(raw)))
    print(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    # nonce = cipher.nonce
    msg= iv + cipher.encrypt(pad(raw))
    return msg


def decrypt(filename,enc,password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    print(private_key)
    # enc = base64.b64decode(enc)
    # iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CBC)
    msg=cipher.decrypt(enc)
    open(filename,'rb').write(msg)

if __name__ == '__main__':
    edata = encrypt('tester', 'kansal123')
    # decrypt('tempout', edata, 'kansal123')