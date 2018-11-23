from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from Crypto.Util.Padding import pad,unpad
from os import stat, remove, rename


# def encrypt(filename, key):
#     bufferSize = 64 * 1024
#     with open(filename, "rb") as fIn:
#         with open(filename + ".aes", 'wb') as fOut:
#             pyAesCrypt.encryptStream(fIn, fOut, key, bufferSize)
#     tempfile = filename + ".aes"
#     with open(tempfile, 'rb') as fRead:
#         remove(tempfile)
#         return fRead.read()
#
#
# def decrypt(filename, data, key):
#     bufferSize = 64 * 1024
#     # with open(filename, "r") as fIn:
#     #     data = fIn.read()
#     #     fIn.seek(0)
#     with open('temp', 'wb') as temp_file:
#         temp_file.write(data)
#         temp_file.close()
#     with open('temp', 'rb') as fIn:
#         encFileSize = stat('temp').st_size
#         with open(filename, "wb") as fOut:
#             try:
#                 pyAesCrypt.decryptStream(fIn, fOut, key, bufferSize, encFileSize)
#             except ValueError:
#                 print("Still an error")
#

block_size = 16


def encrypt(filename, key):
    key = key.encode()
    nkey = SHA256.new(key).digest()
    iv = Random.new().read(block_size)
    cipher = AES.new(nkey, AES.MODE_CBC, iv)
    with open(str(filename), "rb") as fIn:
        raw = fIn.read()
        return iv + cipher.encrypt(pad(raw,block_size))


def decrypt(filename, enc, key):
    key = key.encode()
    nkey = SHA256.new(key).digest()
    iv = enc[:block_size]
    cipher = AES.new(nkey, AES.MODE_CBC, iv)
    dat = unpad(cipher.decrypt(enc[block_size:]),block_size)
    with open(str(filename), 'wb') as fout:
        fout.write(dat)

#
# if _name_ == '_main_':
#     # print(encrypt("Makefile", "hello"))
#     x = encrypt('file1.txt','arkhamknight')
#     decrypt("file1dec.txt",x, "arkhamknight")
#
    # decrypt("test.png.aes", "hello")