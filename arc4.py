# import pyAesCrypt
from os import stat, remove
from Crypto.Cipher import ARC4
from Crypto.Hash import SHA
from Crypto.Random import get_random_bytes

#installed package pycrpto

def arcencrypt(filename, key):
    key=key.encode('ascii')
    with open(filename, "rb") as fIn:
        # nonce=get_random_bytes(16)
        # print(type(key))
        tempkey=SHA.new(key).digest()
        cipher=ARC4.new(tempkey)
        fdata=fIn.read()
        msg=cipher.encrypt(fdata)
        return msg
    

def arcdecrypt(filename, key):
    key = key.encode('ascii')
    with open(filename, "rb") as fIn:
        # tdecrpt=fIn.read()
        # nonce = get_random_bytes(16)
        # print(type(key))
        tempkey = SHA.new(key).digest()
        cipher = ARC4.new(tempkey)
        fdata = fIn.read()
        msg =cipher.decrypt(fdata)
        return msg

if __name__ == '__main__':
    edata=arcencrypt("id.jpeg","hello")
    with open('ns','wb') as fout:
        fout.write(edata)
    ddata=arcdecrypt('ns','hello')
    with open('newimg.jpeg','wb') as fout:
        fout.write(ddata)

