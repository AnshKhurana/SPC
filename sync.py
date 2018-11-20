from os import walk, listdir
from os.path import join, isfile
from apt_pkg import md5sum
import base64
from aes import encrypt
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

def getsubs(mypath):
    flist=[]
    for fname in walk(mypath):
        flist.extend([join(fname[0],f) for f in listdir(fname[0])])
    return flist
def sync2(uname,passwd,obdir,upath,domain):
    pbar=ProgressBar()
    sublist=getsubs(obdir)
    ol=len(obdir.split('/'))
    sublist=map(lambda s: '/'.join(s.split('/')[ol-1:]),sublist)
    r=requests.get('http://'+upath+'/filedatabase')
    jdata=json.loads(r.text)['results']
    mylist=[]
    for i in jdata:
        if i['owner']==uname:
            mylist.append(i)
    # print(mylist)
   #print(list(mylist))
    # print(obdir)
    # print(len(list(sublist)))
    # print("hello")
    # print(len(list(sublist)))
    for f in pbar(list(sublist)):
        # print('hello')
        b=0
        for j in mylist:
            if(j['file_name']==f):
                b=1
                if(j['file_type']=='DIR'):
                    break
                else:
                    if(md5sum(open(obdir+'/'.join(f.split('/')[0:])))!=j['md5sum']):
                        ft = magic.from_file(obdir + '/'.join(f.split('/')[0:]))
                        id1=j['id']
                        fd=encrypt(obdir+'/'.join(f.split('/')[0:]),'hello')
                        msum = md5sum(open(obdir + '/'.join(f.split('/')[0:])))
                        auth = coreapi.auth.BasicAuthentication(username=uname, password=passwd, domain=domain)
                        client = coreapi.Client(auth=auth)
                        document = client.get('http://'+upath + "/schema/")
                        userlist = client.action(document, ['filedatabase', 'update'],
                                                 params={'file_name': f, 'file_type': ft, \
                                                         'file_data': fd, 'md5sum': msum,'id':id1})
                    break
        if(b==0):
            ft=''
            fd=b''
            msum='-'
            if isfile(obdir+'/'.join(f.split('/')[0:])):
                ft=magic.from_file(obdir+'/'.join(f.split('/')[0:]))
                msum=md5sum(open(obdir+'/'.join(f.split('/')[0:])))
                fd=encrypt(obdir+'/'.join(f.split('/')[0:]),'kmvkf')
                # print('hello')
                # print(fd)
            else:
                ft='DIR'
            # print(f)
            # print(len(fd))
            fd=fd+b'='*((4-(len(fd)%4))%4)
            # print(len(fd))
            auth = coreapi.auth.BasicAuthentication(username=uname, password=passwd, domain=domain)
            client = coreapi.Client(auth=auth)
            document = client.get('http://'+upath + "/schema/")
            client.action(document, ['filedatabase', 'create'],params={'file_name':f,'file_type':ft,'file_data':str(fd),'md5sum':msum})
            # print('done')
