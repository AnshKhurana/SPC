from os import walk, listdir
from os.path import join, isfile, expanduser
#from apt_pkg import md5sum
import base64
from arc4 import encrypt
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

myupath = expanduser('~')  # work around


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


def get_status(uname,passwd,obdir,upath,domain):
    prefix_obdir='/'.join(obdir.split('/')[0:-1])+'/'
    aib=[]
    amb=[]
    bma=[]
    cdiff=[]
    sublist=getsubs(obdir)
    ol=len(obdir.split('/'))
    auth = coreapi.auth.BasicAuthentication(username=uname, password=passwd, domain=domain)
    client = coreapi.Client(auth=auth)
    document = client.get('http://' + upath + "/schema/")
    sublist=map(lambda s: '/'.join(s.split('/')[ol-1:]),sublist)
    file_list = []
    pageno = 1
    while True:
        fetched_data = client.action(document, ['filedatabase', 'list'], params={'page': pageno})
        # print(fetched_data)
        pageno = pageno + 1
        file_list = file_list + fetched_data['results']
        # print(fetched_data['next'])
        if fetched_data['next'] == None:
            break
    jdata= file_list
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
                    if md5sumc(prefix_obdir+'/'.join(f.split('/')[0:]))!=j['md5sum']:
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
    print("-----------------")
    print('Files not present locally:')
    for f in bma:
        print(f)
    print("-----------------")
    print('Files with varying content:')
    for f in cdiff:
        print(f)
    print("-----------------")
    print('Files common:')
    for f in aib:
        print(f)
    print("-----------------")

if __name__ == '__main__':
    try:
        with open(myupath + "/config/config.json", "r") as read_file:
            data = json.load(read_file)
            username = data['username']
            password = data['password']
            login_status = data['login']
    except FileNotFoundError:
        print("No user logged in")
    try:
        with open(myupath + "/config/url.json", "r") as read_file:
            data = json.load(read_file)
            server_url = data['server_url']
            domain = data['domain']
    except FileNotFoundError:
        print("Server not set-up")
    try:
        with open(myupath + "/config/path.json", 'r') as read_file:
            data = json.load(read_file)
            observe_path = data['observe_path']
    except:
        print("Directory not set-up")
