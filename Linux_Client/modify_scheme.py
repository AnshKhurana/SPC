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
    if(oldscheme==newscheme):
        return None
    encrypt=0
    decrypt=0
    if(oldscheme=='aes'):
        if(newscheme=='arc4'):
            decrypt=aesdec
            encrypt=arcenc
        else:
            encrypt=blenc
            decrypt=aesdec
    if(oldscheme=='arc4'):
        if(newscheme=='blowfish'):
            decrypt=arcdec
            encrypt=blenc
        else:
            decrypt=arcdec
            encrypt=aesenc
    else:
        if(newscheme=='aes'):
            decrypt=bldec
            encrypt=aesenc
        else:
            decrypt=bldec
            encrypt=arcenc
    auth = coreapi.auth.BasicAuthentication(username=uname, password=passwd, domain=domain)
    client = coreapi.Client(auth=auth)
    document = client.get('http://' + upath + "/schema/")
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
    for i in user_files:
        if i['owner']==uname:
            user_files.append(i)
    for file in user_files:
        if(file['file_type']=='DIR'):
            continue
        decrypt('tempout',literal_eval(file['file_data']),oldkey)
        newdata=encrypt('tempout',newkey)
        auth = coreapi.auth.BasicAuthentication(username=uname, password=passwd, domain=domain)
        client = coreapi.Client(auth=auth)
        document = client.get('http://' + upath + "/schema/")
        userlist = client.action(document, ['filedatabase', 'update'],
                                 params={'file_name': file['file_name'], 'file_type': file['file_type'], \
                                         'file_data': str(newdata), 'md5sum': file['md5sum'], 'id': file['id']})
    if(os.path.exists('tempout')):
        os.remove('tempout')
