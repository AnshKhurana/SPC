from os import walk, listdir
from os.path import join, isfile

import base64

from aes import encrypt
import coreapi
import magic
import requests
import json

from apt_pkg import md5sum

uname='pk'
passwd='lokikoli'
obdir='/home/aman/Desktop/machine-learning-ex8'
upath='127.0.0.1:8000'
def getsubs(mypath):
    # mypath='/home/aman/Desktop/machine-learning-ex8'
    flist=[]
    # onlyfiles=[f for f in listdir(walk('/home/aman/Desktop/SPC')) if\
    #                               isfile(join(mypath,f))]
    # print(walk(mypath))
    for fname in walk(mypath):
        # print(fname)
        flist.extend([join(fname[0],f) for f in listdir(fname[0])])

        # print(fname[0])
        # x=2
    return flist
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
print(list(mylist))
for f in sublist:
    b=0
    for j in mylist:
        if(j['file_name']==f):
            b=1
            if(j['file_type']=='DIR'):
                break
            else:
                if(md5sum(open(obdir+'/'+'/'.join(f.split('/')[1:])))!=j['md5sum']):
                    ft = magic.from_file(obdir + '/'.join(f.split('/')[1:]))
                    id1=j['id']
                    fd=encrypt(obdir+'/'+'/'.join(f.split('/')[1:]),'hello')
                    msum = md5sum(open(obdir+'/' + '/'.join(f.split('/')[1:])))
                    auth = coreapi.auth.BasicAuthentication(username=uname, password=passwd, domain='127.0.0.1')
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
        if isfile(obdir+'/'+'/'.join(f.split('/')[1:])):
            ft=magic.from_file(obdir+'/'+'/'.join(f.split('/')[1:]))
            msum=md5sum(open(obdir+'/'+'/'.join(f.split('/')[1:])))
            fd=encrypt(obdir+'/'+'/'.join(f.split('/')[1:]),'kmvkf')
            # print('hello')
            # print(fd)
        else:
            ft='DIR'
        # print(f)
        # print(len(fd))
        fd=fd+b'='*((4-(len(fd)%4))%4)
        # print(len(fd))
        auth = coreapi.auth.BasicAuthentication(username=uname, password=passwd, domain='127.0.0.1')
        client = coreapi.Client(auth=auth)
        document = client.get('http://'+upath + "/schema/")
        client.action(document, ['filedatabase', 'create'],params={'file_name':f,'file_type':ft,'file_data':str(fd),'md5sum':msum})
        # print('done')

