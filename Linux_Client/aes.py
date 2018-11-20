import pyAesCrypt
from os import stat, remove

def encrypt(filename, key):
    bufferSize = 64 * 1024
    with open(filename, "rb") as fIn:
        with open(filename + ".aes", 'wb') as fOut:
            pyAesCrypt.encryptStream(fIn, fOut, key, bufferSize)
    tempfile = filename + ".aes"
    with open(tempfile, 'rb') as fRead:
        remove(tempfile)
        return fRead.read()
    
#
# def decrypt(filename, key):
#     bufferSize = 64 * 1024
#     encFileSize = stat(filename).st_size
#     with open(filename, "rb") as fIn:
#         with open("decrypted", "wb") as fOut:
#             try:
#                 # decrypt file stream
#                 pyAesCrypt.decryptStream(fIn, fOut, key, bufferSize, encFileSize)
#             except ValueError:
#                 # remove output file on error
#                 remove("dataout.txt")
#


def decrypt(filename, data, key):
    bufferSize = 64 * 1024
    encFileSize = stat(filename).st_size
    with open(filename, "wb+") as fIn:
        with open():
            try:
                pyAesCrypt.decryptStream(fIn, fIn, key, bufferSize, encFileSize)
            except ValueError:
                print("A Value Error occurred")

if __name__ == '__main__':
    print(encrypt("Makefile", "hello"))
    #decrypt("test.png.aes", "hello")
