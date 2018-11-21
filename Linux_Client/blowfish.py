from Crypto.Cipher import Blowfish
from struct import pack
from Crypto import Random



def encrypt(filename, key):
    bs=Blowfish.block_size
    key=key.encode('ascii')
    iv=Random.new().read(bs)
    cipher=Blowfish.new(key,Blowfish.MODE_CBC,iv)
    pdata=open(filename,'rb').read()
    plen=bs-divmod(len(pdata),bs)[1]
    padding=[plen]*plen
    padding=pack('b'*plen,*padding)
    return iv+cipher.encrypt(pdata+padding)

def decrypt(filename, key):
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
    print(msg)
    return msg


if __name__ == '__main__':
    edata = encrypt("Makefile", "hellorrrlmnkhmnk")
    with open('ns', 'wb') as fout:
        fout.write(edata)
    ddata = decrypt('ns', 'hellorrrlmnkhmnk')
    with open('newMakefile', 'wb') as fout:
        fout.write(ddata)
