from os import walk, listdir
from os.path import join, isfile
#from apt_pkg import md5sum
import base64
import hashlib
import coreapi
import magic
import requests
import json
from progressbar import ProgressBar
from arc4 import encrypt, decrypt
# import hashlib
# uname='pk'
# passwd='lokikoli'
# obdir='/home/aman/Desktop/machine-learning-ex8'
# upath='127.0.0.1:8000'


def choose_scheme(id):
    if id==1:
        from aes import encrypt, decrypt
    elif id==2:
        from arc4 import encrypt, decrypt
    elif id==3:
        from blowfish import encrpyt, decrypt


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
    choose_scheme(2)
    pbar=ProgressBar()
    sublist = getsubs(obdir)
    ol=len(obdir.split('/'))
    sublist = map(lambda s: '/'.join(s.split('/')[ol-1:]), sublist)
    auth = coreapi.auth.BasicAuthentication(username=uname, password=passwd, domain=domain)
    client = coreapi.Client(auth=auth)
    document = client.get('http://' + upath + "/schema/")
    file_list = client.action(document, ['filedatabase', 'list'])
    file_list = file_list['results']
    jdata=file_list
    mylist=[]
    #print([x['file_name'] for x in jdata])
    #print('--------------------')
    for i in jdata:
        if i['owner']==uname:
            mylist.append(i)
    #print(mylist)
    #print(list(mylist))
    # print(obdir)
    # print(len(list(sublist)))
    # print("hello")
    # print(len(list(sublist)))
    sl=list(sublist)
    print(sl)
    print('--------------------')
    print([x['file_name'] for x in mylist])
    for f in pbar(sl):
        # print('hello')
        b=0
        # print(f)
        for j in mylist:
            # if(f=='abc/temp.txt'):
            #     print(j['file_name'])
            if(j['file_name']==f):
                b=1
                if(j['file_type']=='DIR'):
                    break
                else:
                    # print('/'.join(f.split('/')[0:]))
                    # print(md5sumc('/'.join(f.split('/')[0:])))
                    if md5sumc('/'.join(f.split('/')[0:]))!=j['md5sum']:
                        # print('entered')
                        ft = magic.from_file('/'.join(f.split('/')[0:]))
                        id1=j['id']
                        fd=encrypt('/'.join(f.split('/')[0:]),passwd)
                        # fd = fd + b'=' * ((4 - (len(fd) % 4)) % 4)
                        msum = md5sumc('/'.join(f.split('/')[0:]))
                        # print(msum)
                        auth = coreapi.auth.BasicAuthentication(username=uname, password=passwd, domain=domain)
                        client = coreapi.Client(auth=auth)
                        document = client.get('http://'+upath + "/schema/")
                        userlist = client.action(document, ['filedatabase', 'update'],
                                                 params={'file_name': f, 'file_type': ft, \
                                                         'file_data': str(fd), 'md5sum': msum,'id':id1})

                    break
        if(b==0):
            # print(f)
            ft=''
            fd=b''
            msum='-'
            # print(obdir+'/'.join(f.split('/')[0:]))
            if isfile('/'.join(f.split('/')[0:])):
                ft=magic.from_file('/'.join(f.split('/')[0:]))
                # print('/'.join(f.split('/')[0:]))
                # print(ft)
                msum=md5sumc('/'.join(f.split('/')[0:]))
                fd=encrypt('/'.join(f.split('/')[0:]),passwd)

            else:
                ft='DIR'
            # print(f)
            # print(len(fd))
            # fd=fd+b'='*((4-(len(fd)%4))%4)
            # print(len(fd))
            auth = coreapi.auth.BasicAuthentication(username=uname, password=passwd, domain=domain)
            client = coreapi.Client(auth=auth)
            document = client.get('http://'+upath + "/schema/")
            client.action(document, ['filedatabase', 'create'],params={'file_name':f,'file_type':ft,'file_data':str(fd),'md5sum':msum})
            # print('done')



if __name__ == '__main__':
    print(md5sumc('requirements.txt'))
