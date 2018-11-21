import pyAesCrypt
from tempfile import TemporaryFile
from os import stat, remove, rename
import io


def encrypt(filename, key):
    bufferSize = 64 * 1024
    with open(filename, "rb") as fIn:
        with open(filename + ".aes", 'wb') as fOut:
            pyAesCrypt.encryptStream(fIn, fOut, key, bufferSize)
    tempfile = filename + ".aes"
    with open(tempfile, 'rb') as fRead:
        remove(tempfile)
        return fRead.read()


def decrypt(filename, data, key):
    bufferSize = 64 * 1024
    # with open(filename, "r") as fIn:
    #     data = fIn.read()
    #     fIn.seek(0)
    with open('temp', 'w') as temp_file:
        temp_file.write(data)
        temp_file.close()
    with open('temp', 'rb') as temp_file:
        encFileSize = stat('temp').st_size
        with open(filename, "wb") as fOut:
            try:
                # decrypt file stream
                print(temp_file.read())
                temp_file.seek(0)
                pyAesCrypt.decryptStream(temp_file, fOut, key, bufferSize, encFileSize)
            except ValueError:
                print("Still an error")


#
# def decrypt(filename, key):
#     bufferSize = 64 * 1024
#     # with TemporaryFile() as fIn:
#     #     fIn.write(bytes(data, 'UTF-8'))
#     #     print(fIn.read())
#     encFileSize = stat(filename).st_size
#     with open(filename, 'w+', encoding='utf-8') as fIn:
#         fIn.write(data)
#         fIn.seek(0)
#         print(fIn.read())
#         fIn.seek(0)
#         with open('temp', 'w+b') as fOut:
#             pyAesCrypt.decryptStream(fIn, fOut, key, bufferSize, encFileSize)
#     rename('temp', filename)


if __name__ == '__main__':
    # print(encrypt("Makefile", "hello"))
    decrypt("abc/Makefile", "arkhamknight")

    # decrypt("test.png.aes", "hello")
