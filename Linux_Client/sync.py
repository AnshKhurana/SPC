from ast import literal_eval
from os import walk, listdir
from os.path import join, isfile, expanduser
import hashlib
import coreapi
import magic
import json
import requests
from progressbar import ProgressBar

# EN-DE Variables

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
    uid = None
    for i in jdata:
        if i['owner']==uname:
            mylist.append(i)
    sl=list(sublist)
    # print(sl)
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

            local_md = (hashlib.md5(fd).hexdigest())


            client.action(document, ['filedatabase', 'create'],params={'file_name':f,'file_type':ft,'file_data':str(fd),'md5sum':msum})
            result = requests.get(upath + "/md5/?id=" +  )
            # print('done')



if __name__ == '__main__':
    print(md5sumc('requirements.txt'))