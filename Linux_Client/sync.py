
import urllib
from ast import literal_eval
from os import walk, listdir
from os.path import join, isfile, expanduser
import hashlib
import coreapi
import magic
import json
import requests
from progressbar import ProgressBar
import signal
# EN-DE Variables
class TimeoutException(Exception):   # Custom exception class
    pass

def timeout_handler(signum, frame):   # Custom signal handler
    raise TimeoutException
signal.signal(signal.SIGALRM, timeout_handler)
schema_id = None
schema_name = None
sym_key = None
public_key = None
private_key = None
IDS = {"RSA": 4, "AES": 1, "ARC4": 2, "Blowfish": 3}


myupath = expanduser('~')  # work around

def read_schema():
    global schema_id
    global schema_name
    global sym_key
    try:
        with open(myupath + "/config/scheme.json", "r") as read_file:
            data = json.load(read_file)
            schema_id = data['ID']
            schema_name = data['Scheme_Name']
            sym_key = data['Symmetric_Key']
            #  print(schema_id)
           #choose_scheme(schema_id)
    except FileNotFoundError:
        print("Need to set the schema before this operation")




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
    prefix_obdir='/'.join(obdir.split('/')[0:-1])+'/'
    # print(prefix_obdir)
    # print('here')
    read_schema()
    if schema_id==1:
        from aes import encrypt
    elif schema_id==2:
        from arc4 import encrypt
    elif schema_id==3:
        from blowfish import encrypt
    pbar=ProgressBar()
    sublist = getsubs(obdir)
    ol=len(obdir.split('/'))
    sublist = map(lambda s: '/'.join(s.split('/')[ol-1:]), sublist)
    auth = coreapi.auth.BasicAuthentication(username=uname, password=passwd, domain=domain)
    client = coreapi.Client(auth=auth)
    document = client.get('http://' + upath + "/schema/")
    uid = None
    count = 0
    user_list = []
    pageno = 1
    while True:
        fetched_data = client.action(document, ['users', 'list'], params={'page': pageno})
        # print(fetched_data)
        pageno = pageno + 1
        user_list = user_list + fetched_data['results']
        # print(fetched_data['next'])
        if fetched_data['next'] == None:
            break
    # print(user_list)
    is_active = 0
    for person in user_list:
        if person['username'] == uname:
            uid = person['id']
            is_active = person['cur_active']
            break
    if is_active:
        print("Sorry, a sync is already active for given user.")
    else:
        is_active = 1
        client.action(document, ['users', 'partial_update'], params={'id':uid,'cur_active': True})

    uid = str(uid)
    file_list = []
    pageno=1
    while True:
        fetched_data = client.action(document, ['filedatabase', 'list'], params={'page' : pageno})
        #print(fetched_data)
        pageno = pageno + 1
        file_list = file_list + fetched_data['results']
        #print(fetched_data['next'])
        if fetched_data['next'] == None:
            break
    jdata=file_list
    mylist=[]
    #print([x['file_name'] for x in jdata])
    #print('--------------------')
    for i in jdata:
        if i['owner']==uname:
            # uid = i['owner_id']
            mylist.append(i)
    sl=list(sublist)
    # print(sl)
    for f in pbar(sl):
        # print('hello')
        b=0
        # print(f)
        signal.alarm(10)
        try:
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
                        if md5sumc(prefix_obdir+'/'.join(f.split('/')[0:]))!=j['md5sum']:
                            # print('entered')
                            ft = magic.from_file(prefix_obdir+'/'.join(f.split('/')[0:]))
                            id1=j['id']
                            fd=encrypt(prefix_obdir+'/'.join(f.split('/')[0:]), sym_key)
                            # fd = fd + b'=' * ((4 - (len(fd) % 4)) % 4)
                            msum = md5sumc(prefix_obdir+'/'.join(f.split('/')[0:]))
                            # print(msum)
                            auth = coreapi.auth.BasicAuthentication(username=uname, password=passwd, domain=domain)
                            client = coreapi.Client(auth=auth)
                            document = client.get('http://'+upath + "/schema/")
                            print(hashlib.md5(fd).hexdigest())
                            userlist = client.action(document, ['filedatabase', 'update'],
                                                     params={'file_name': f, 'file_type': ft, \
                                                             'file_data': str(fd), 'md5sum': msum,'id':id1})
                            local_md = (hashlib.md5(fd).hexdigest())
                            # print(upath, uid, f)
                            server_md = requests.get("http://" + upath + "/md5/?ownerid=" + uid + "&filename=" + urllib.parse.quote_plus(f))
                            server_md = server_md.json()['md5']
                            if local_md != server_md:
                                count = count + 1

                        break
            if(b==0):
                # print(f)
                ft=''
                fd=b''
                msum='-'
                # print(obdir+'/'.join(f.split('/')[0:]))
                if isfile(prefix_obdir+'/'.join(f.split('/')[0:])):
                    ft=magic.from_file(prefix_obdir+'/'.join(f.split('/')[0:]))
                    # print('/'.join(f.split('/')[0:]))
                    # print(ft)
                    msum=md5sumc(prefix_obdir+'/'.join(f.split('/')[0:]))
                    fd=encrypt(prefix_obdir+'/'.join(f.split('/')[0:]), sym_key)

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

                local_md = (hashlib.md5(fd).hexdigest())
                # print(upath, uid, f)
                # print(uid)
                server_md = requests.get("http://" + upath + "/md5/?ownerid=" + uid + "&filename=" + urllib.parse.quote_plus(f))
                server_md = server_md.json()["md5"]

                if local_md != server_md:
                    count = count + 1
        except:
            print("Error in uploading files")
            new_file_list = []
            pageno = 1
            while True:
                fetched_data = client.action(document, ['filedatabase', 'list'], params={'page': pageno})
                # print(fetched_data)
                pageno = pageno + 1
                new_file_list = new_file_list + fetched_data['results']
                # print(fetched_data['next'])
                if fetched_data['next'] == None:
                    break
            for newfile in new_file_list:
                if(newfile['owner']==uname):
                    client.action(document,['filedatabase','delete'],params={'id':newfile['id']})
            for oldfile in mylist:
                client.action(document, ['filedatabase', 'create'],
                              params={'file_name': oldfile['file_name'], 'file_type': oldfile['file_type']\
                                  , 'file_data': oldfile['file_data'], 'md5sum':oldfile['md5sum']})
            #user files delete
            #mylist files upload
            client.action(document, ['users', 'partial_update'], params={'id': uid, 'cur_active': False})
            return None

    if count == 0:
        print("Files were uploaded correctly and verified with md5sum")
    else:
        print("Files were not uploaded correctly, please retry.")
    # print('done')
    client.action(document, ['users', 'partial_update'], params={'id': uid, 'cur_active': False})


if __name__ == '__main__':
    # print(md5sumc('requirements.txt'))
    # sublist = map(lambda s: '/'.join(s.split('/')[ol - 1:]), sublist)
    auth = coreapi.auth.BasicAuthentication(username="ansh", password="arkhamknight", domain="10.196.16.186")
    client = coreapi.Client(auth=auth)
    document = client.get('http://' + "10.196.16.186:8000" + "/schema/")
    client.action(document, ['users', 'partial_update'], params={"id" : 4, "cur_active" : 1})
    user_list = []
    pageno = 1
    while True:
        fetched_data = client.action(document, ['users', 'list'], params={'page': pageno})
        # print(fetched_data)
        pageno = pageno + 1
        user_list = user_list + fetched_data['results']
        # print(fetched_data['next'])
        if fetched_data['next'] == None:
            break
    # print(user_list)
    is_active = 0
    for person in user_list:
        if person['username'] == "ansh":
            uid = person['id']
            is_active = person['cur_active']
            break
    print(uid, is_active)
