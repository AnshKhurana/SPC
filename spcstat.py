from os import walk, listdir
from os.path import join, isfile
#from apt_pkg import md5sum
import base64
from aes import encrypt
import hashlib
import coreapi
import magic
import requests
import json
from progressbar import ProgressBar
# import hashlib
# uname='pk'
# passwd='lokikoli'
# obdir='/home/aman/Desktop/machine-learning-ex8'
# upath='127.0.0.1:8000'


def md5sumc(filename):
    with open(filename, 'rb') as file_to_check:
        # read contents of the file
        data = file_to_check.read()
        # pipe contents of the file through
        md5_returned = hashlib.md5(data).hexdigest()
        return md5_returned


def getsubs(mypath):
    flist=[]
    for fname in walk(mypath):
        flist.extend([join(fname[0],f) for f in listdir(fname[0])])
    return flist


def sync2(uname,passwd,obdir,upath,domain):
    aib=[]
    amb=[]
    bma=[]
    cdiff=[]
    sublist=getsubs(obdir)
    ol=len(obdir.split('/'))
    sublist=map(lambda s: '/'.join(s.split('/')[ol-1:]),sublist)
    r=requests.get('http://'+upath+'/filedatabase')
    jdata=json.loads(r.text)['results']
    mylist=[]
    for i in jdata:
        if i['owner']==uname:
            mylist.append(i)
    sl=list(sublist)
    for f in sl:
        b=0
        for j in mylist:
            if(j['file_name']==f):
                b=1
                if(j['file_type']=='DIR'):
                    aib.append(f)
                    break
                else:
                    if md5sumc('/'.join(f.split('/')[0:]))!=j['md5sum']:
                        cdiff.append(f)
                    else:
                        aib.append(f)
                        break
        if(b==0):
            amb.append(f)
    for j in mylist:
        b=0
        for f in sl:
            if(f==j['file_name']):
                b=1
        if(b==0):
            bma.append(j['file_name'])
    print('Files not present on the drive:')
    for f in amb:
        print(f)
    print('Files not present locally:')
    for f in bma:
        print(f)
    print('Files with varying content:')
    for f in cdiff:
        print(f)
    print('Files common:')
    for f in aib:
        print(f)


if __name__ == '__main__':
    print(md5sumc('requirements.txt'))