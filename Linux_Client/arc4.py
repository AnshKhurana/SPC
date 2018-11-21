from Crypto.Cipher import ARC4
from Crypto.Hash import SHA

def encrypt(filename, key):
    key = key.encode('ascii')
    with open(filename, "rb") as fIn:
        # nonce=get_random_bytes(16)
        # print(type(key))
        tempkey = SHA.new(key).digest()
        cipher = ARC4.new(tempkey)
        fdata = fIn.read()
        msg = cipher.encrypt(fdata)
        return msg

def decrypt(filename, data, key):
    key = key.encode('ascii')
    # with open(filename, "rb") as fIn:
        # tdecrpt=fIn.read()
        # nonce = get_random_bytes(16)
        # print(type(key))
    tempkey = SHA.new(key).digest()
    cipher = ARC4.new(tempkey)
    fdata = data
    msg = cipher.decrypt(fdata)
    print("hello"+msg)
    # return msg
    with open(filename,'wb') as fout:
        fout.write(msg)


if __name__ == '__main__':
    edata = encrypt("Makefile", "hello")
    with open('ns', 'wb') as fout:
        fout.write(edata)
    ddata = decrypt('ns', 'hello')
    with open('newMakefile', 'wb') as fout:
        fout.write(ddata)