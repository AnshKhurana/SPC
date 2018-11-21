from Crypto.Cipher import ARC4
from Crypto.Hash import SHA


def encrypt(filename, key):
    key = key.encode()
    with open(filename, "rb") as fIn:
        tempkey = SHA.new(key).digest()
        cipher = ARC4.new(tempkey)
        fdata = fIn.read()
        msg = cipher.encrypt(fdata)
        return msg


def decrypt(filename, data, key):
    key = key.encode()
    tempkey = SHA.new(key).digest()
    cipher = ARC4.new(tempkey)
    fdata = data
    msg = cipher.decrypt(fdata)
    with open(filename, 'wb') as fout:
        fout.write(msg)


if __name__ == '__main__':
    edata = encrypt("Makefile", "arkhamknight")
    with open('ns', 'wb') as fout:
        fout.write(edata)
    decrypt('ns', edata, 'arkhamknight')
