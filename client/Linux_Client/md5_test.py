import os
import hashlib


def md5sum(filename):
    with open(filename, 'r') as file_to_check:
        # read contents of the file
        data = file_to_check.read().encode('utf-8')
        # pipe contents of the file through
        md5_returned = hashlib.md5(data).hexdigest()
        return md5_returned

if __name__ == '__main__':
    print(md5sum("abc/file1.txt"))