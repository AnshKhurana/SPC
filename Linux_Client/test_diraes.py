from Crypto.Cipher import ARC4
from Crypto.Hash import SHA
from ast import literal_eval

def encrypt(filename, key):
    key = key.encode()
    with open(filename, "rb") as fIn:
        # nonce=get_random_bytes(16)
        # print(type(key))
        tempkey = SHA.new(key).digest()
        cipher = ARC4.new(tempkey)
        fdata = fIn.read()
        msg = cipher.encrypt(fdata)
        return msg


def decrypt(filename, data, key):
    key = key.encode()
    # with open(filename, "rb") as fIn:
    # tdecrpt=fIn.read()
    # nonce = get_random_bytes(16)
    # print(type(key))
    tempkey = SHA.new(key).digest()
    cipher = ARC4.new(tempkey)
    fdata = literal_eval(data)
    print(fdata,type(fdata))
    msg = cipher.decrypt(fdata)
    print('hello')
    #print(type(msg.decode('ascii')))
    # return msg
    with open(filename, 'wb') as fout:
        fout.write(msg)


if __name__ == '__main__':
    edata = encrypt("file1.txt", "arkhamknight")
    print(str(edata)[2:-1])
    decrypt('temp.txt',str(edata),"arkhamknight")