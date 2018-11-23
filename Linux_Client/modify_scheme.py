import os

import coreapi
from ast import literal_eval

from aes import encrypt as aesenc
from aes import decrypt as aesdec
from arc4 import encrypt as arcenc
from arc4 import decrypt as arcdec
from blowfish import encrypt as blenc
from blowfish import decrypt as bldec

def schema_update(uname, passwd, upath, domain, oldscheme, newscheme, oldkey, newkey):
    print("upath is: " + upath)
    if(oldscheme==newscheme and oldkey==newkey):
        return None
    encrypt=0
    decrypt=0
    if(oldscheme==newscheme):
        if(oldscheme=='AES'):
            # print('yo yp')
            encrypt=aesenc
            decrypt=aesdec
        elif(oldscheme=='ARC4'):
            encrypt=arcenc
            decrypt=arcdec
        else:
            encrypt=blenc
            decrypt=bldec
    elif(oldscheme=='AES'):
        if(newscheme=='ARC4'):
            decrypt=aesdec
            encrypt=arcenc
        else:
            encrypt=blenc
            decrypt=aesdec
    elif(oldscheme=='ARC4'):
        if(newscheme=='Blowfish'):
            decrypt=arcdec
            encrypt=blenc
        else:
            decrypt=arcdec
            encrypt=aesenc
    else:
        if(newscheme=='AES'):
            decrypt=bldec
            encrypt=aesenc
        else:
            decrypt=bldec
            encrypt=arcenc
    try:
        auth = coreapi.auth.BasicAuthentication(username=uname, password=passwd, domain=domain)
        client = coreapi.Client(auth=auth)
        document = client.get('http://' + upath + "/schema/")
    except:
        print("Authentication failed.")
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
    user_files=[]
    for i in file_list:
        if i['owner']==uname:
            user_files.append(i)
    for file in user_files:
        # print('here')
        if(file['file_type']=='DIR'):
            continue
        decrypt('tempout',literal_eval(file['file_data']),oldkey)
        newdata=encrypt('tempout',newkey)

        try:
            auth = coreapi.auth.BasicAuthentication(username=uname, password=passwd, domain=domain)
            client = coreapi.Client(auth=auth)
            document = client.get('http://' + upath + "/schema/")
        except:
            print("Authentication failed")

        userlist = client.action(document, ['filedatabase', 'update'],
                                 params={'file_name': file['file_name'], 'file_type': file['file_type'], \
                                         'file_data': str(newdata), 'md5sum': file['md5sum'], 'id': file['id']})
    if(os.path.exists('tempout')):
        os.remove('tempout')
