# AES 256 encryption/decryption using pycrypto library

import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

# password = input("Enter encryption password: ")


def encrypt(filename, password):
    private_key = hashlib.sha256(password.encode()).digest()
    raw=open(filename,'rb').read()
    # print(type(raw))
    # raw = pad(raw)
    # iv = Random.new().read(AES.block_size)

    cipher = AES.new(private_key,AES.MODE_CBC)
    nonce=cipher.nonce
    msg=cipher.encrypt(raw)

    return msg


def decrypt(filename,enc,password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    # enc = base64.b64decode(enc)
    # iv = enc[:16]
    cipher = AES.new(private_key,AES.MODE_CBC)
    msg=cipher.decrypt(enc)
    open(filename,'rb').write(msg)

edata=encrypt('id.jpeg','kansal123')
decrypt('tempout.jpeg',edata,'kansal123')
