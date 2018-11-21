# import pyAesCrypt
from os import stat, remove
from Crypto.Cipher import Blowfish
from struct import pack
from Crypto import Random
# from Crypto.Random import get_random_bytes


# installed package pycrpto

def blowencrypt(filename, key):
    bs=Blowfish.block_size
    key=key.encode('ascii')
    iv=Random.new().read(bs)
    cipher=Blowfish.new(key,Blowfish.MODE_CBC,iv)
    pdata=open(filename,'rb').read()
    plen=bs-divmod(len(pdata),bs)[1]
    padding=[plen]*plen
    padding=pack('b'*plen,*padding)
    return iv+cipher.encrypt(pdata+padding)

def blowdecrypt(filename, key):
    bs = Blowfish.block_size
    key = key.encode('ascii')
    pdata = open(filename, 'rb').read()
    iv = pdata[:bs]
    pdata=pdata[bs:]
    cipher = Blowfish.new(key, Blowfish.MODE_CBC,iv)
    # plen = bs - len(pdata) % bs
    # padding = [plen] * plen
    # padding = pack('b' * plen, *padding)
    msg = cipher.decrypt(pdata)
    last_byte = msg[-1]

    msg = msg[:- (last_byte if type(last_byte) is int else ord(last_byte))]
    return msg


if __name__ == '__main__':
    edata = blowencrypt("id.jpeg", "hellorrrlmnkhmnk")
    with open('ns', 'wb') as fout:
        fout.write(edata)
    ddata = blowdecrypt('ns', 'hellorrrlmnkhmnk')
    with open('newimg.jpeg', 'wb') as fout:
        fout.write(ddata)

