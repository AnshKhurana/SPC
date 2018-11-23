import argparse
import urllib

import coreapi
import getpass
import json
import os
import hashlib
from pathlib import Path

import requests
from sync import sync2

from file_status import get_status

from modify_scheme import schema_update

from ast import literal_eval
from progressbar import ProgressBar
parser = argparse.ArgumentParser(prog='spc')

# coreapi variables

client = None
document = None

# Status variables

server_url = None
domain = None
login_status = False
observe_path = None

# User details

username = None
password = None

# EN-DE Variables

schema_id = None
schema_name = None
sym_key = None
public_key = None
private_key = None
IDS = {"AES": 1, "ARC4": 2, "Blowfish": 3}

myupath = os.path.expanduser('~')  # work around

parser.add_argument("--status", help="Current status of client", action="store_true")
parser.add_argument("--sync", help="Syncs the user with the client.", action="store_true")
parser.add_argument('--version', action='version', version='%(prog)s 0.7')
parser.add_argument("--observe", help="Observe a directory")
parser.add_argument("--login", help="Check if fields are filled", action="store_true")
parser.add_argument("--download", action="store_true", help="A subprocess to download the files. (Use with caution)")
parser.add_argument("--upload", action="store_true", help="A subprocess to upload the files. (Use with caution)")
parser.add_argument("--delete", action="store_true", help="Delete files from the database. (Use with caution)")

subparsers = parser.add_subparsers(help='Specify secondary options', dest='sub')

parser_server = subparsers.add_parser("server", help='Server sub-commands')
parser_ende = subparsers.add_parser('en-de', help='en-de sub-commands')
parser_config = subparsers.add_parser('config', help='config sub-commands')

parser_server.add_argument('--set_url', action="store_true", help="Set up url of the server")
parser_server.add_argument('--disconnect', action="store_true", help="Remove server")

parser_ende.add_argument('--list', action="store_true", help="List the available encryption schemes")
parser_ende.add_argument('--update', action="store_true", help="Update the encryption scheme")
parser_ende.add_argument('--dump', action="store_true", help="Dump current scheme")
parser_ende.add_argument('--file', '-f', help="specify a file")
parser_ende.add_argument('--view', action='store_true', help="View the current scheme")

parser_config.add_argument('--delete', action="store_true", help="Delete current credentials")
parser_config.add_argument('--edit', action='store_true', help="Edit your credentials")


def choose_scheme(id):
    if id==1:
        from aes import decrypt
    elif id==2:
        from arc4 import decrypt
    elif id==3:
        from blowfish import decrypt

def md5sum(filename):
    with open(str(filename), 'rb') as file_to_check:
        # read contents of the file
        data = file_to_check.read()
        # pipe contents of the file through
        md5_returned = hashlib.md5(data).hexdigest()
        return md5_returned

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
          #  choose_scheme(schema_id)
    except FileNotFoundError:
        print("Need to set the schema before this operation.")



def update_scheme_file(filename):
    global schema_id
    global schema_name
    global sym_key
    global username
    global password
    global server_url
    global domain
    updated = False
    try:
        try:
            with open(myupath + "/config/config.json", "r") as read_file:
                data = json.load(read_file)
                username = data['username']
                password = data['password']
                login_status = data['login']
        except FileNotFoundError:
            print("Use config --edit to login")
            return None
        try:
            with open(myupath + "/config/url.json", "r") as read_file:
                data = json.load(read_file)
                server_url = data['server_url']
                domain = data['domain']
        except FileNotFoundError:
            print("Use server --set_url to connect")
            return None
        try:
            auth = coreapi.auth.BasicAuthentication(username=username, password=password, domain=domain)
            client = coreapi.Client(auth=auth)
            document = client.get("http://" + server_url + "/schema/")
        except:
            print("Authentication failed.")
            return None

        with open(myupath + "/config/scheme.json", "r") as read_file:
            data = json.load(read_file)
            old_id = data['ID']
            old_schema_name = data['Scheme_Name']
            old_sym_key = data['Symmetric_Key']
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    content = f.read().splitlines()
                    if content[0] in ['AES', 'ARC4', 'Blowfish']:
                        schema_name = content[0]
                        schema_id = IDS[schema_name]
                        sym_key = content[1]
                        data = {"ID": schema_id, "Scheme_Name": schema_name, "key-gen": 'NA', "Symmetric_Key": sym_key, \
                                "Public_Key": 'NA', "Private_Key": 'NA'}
                        if os.path.exists(myupath + "/config/"):
                            with open(myupath + "/config/scheme.json", "w") as write_file:
                                json.dump(data, write_file)
                                updated = True
                        else:
                            os.makedirs(myupath + "/config/")
                            with open(myupath + "/config/scheme.json", "w") as write_file:
                                json.dump(data, write_file)
                                updated = True
                    else:
                        print("Invalid file format. The first line must be a valid encryption scheme")
            else:
                print("Invalid file path")

            if updated:
                print("Encryption schema has been updated according to " + filename)
            schema_update(username, password, server_url, domain, old_schema_name, schema_name, old_sym_key, sym_key)
    except FileNotFoundError:
        if os.path.exists(filename):
            with open(str(filename), 'r') as f:
                content = f.read().splitlines()
                if content[0] in ['AES', 'ARC4', 'Blowfish']:
                    schema_name = content[0]
                    schema_id = IDS[schema_name]
                    sym_key = content[1]
                    data = {"ID": schema_id, "Scheme_Name": schema_name, "key-gen": 'NA', "Symmetric_Key": sym_key, \
                            "Public_Key": 'NA', "Private_Key": 'NA'}
                    if os.path.exists(myupath + "/config/"):
                        with open(myupath + "/config/scheme.json", "w") as write_file:
                            json.dump(data, write_file)
                            updated = True
                    else:
                        os.makedirs(myupath + "/config/")
                        with open(myupath + "/config/scheme.json", "w") as write_file:
                            json.dump(data, write_file)
                            updated = True
                else:
                    print("Invalid file format. The first line must be a valid encryption scheme")
        else:
            print("Invalid file path")

        if updated:
            print("Encryption schema has been updated according to " + filename)


def update_schema():
    global schema_id
    global schema_name
    global sym_key
    global username
    global password
    global server_url
    global domain
    try:
        try:
            with open(myupath + "/config/config.json", "r") as read_file:
                data = json.load(read_file)
                username = data['username']
                password = data['password']
                login_status = data['login']
        except FileNotFoundError:
            print("Use config --edit to login")
            return None
        try:
            with open(myupath + "/config/url.json", "r") as read_file:
                data = json.load(read_file)
                server_url = data['server_url']
                domain = data['domain']
        except FileNotFoundError:
            print("Use server --set_url to connect.")
            return None
        # auth = coreapi.auth.BasicAuthentication(username=username, password=password, domain=domain)
        # client = coreapi.Client(auth=auth)
        # document = client.get("http://" + server_url + "/schema/")
        with open(myupath + "/config/scheme.json", "r") as read_file:
            data = json.load(read_file)
            old_id = data['ID']
            old_schema_name = data['Scheme_Name']
            old_sym_key = data['Symmetric_Key']
            print("Schema update")
            list_schemes()
            print("")
            while True:
                schema_name = input("Enter a scheme name: ")
                if schema_name in ['RSA', 'AES', 'ARC4', 'Blowfish']:
                    break
                else:
                    print("Schema name is not valid, enter the scheme name from the above list(case sensitive)")

            schema_id = IDS[schema_name]
            sym_key = input("Enter the key for your encryption scheme: ")
            data = {"ID": schema_id, "Scheme_Name": schema_name, "key-gen": 'NA', "Symmetric_Key": sym_key, \
                    "Public_Key": 'NA', "Private_Key": 'NA'}
            if os.path.exists(myupath + "/config/"):
                with open(myupath + "/config/scheme.json", "w") as write_file:
                    json.dump(data, write_file)
            else:
                os.makedirs(myupath + "/config/")
                with open(myupath + "/config/scheme.json", "w") as write_file:
                    json.dump(data, write_file)
            schema_update(username, password, server_url, domain, old_schema_name, schema_name, old_sym_key, sym_key)
    except FileNotFoundError:
        print("Schema update")
        list_schemes()
        print("")
        while True:
            schema_name = input("Enter a scheme name: ")
            if schema_name in ['AES', 'ARC4', 'Blowfish']:
                break
            else:
                print("Schema name is not valid, enter the scheme name from the above list(case sensitive)")

        schema_id = IDS[schema_name]
        sym_key = input("Enter the key for your encryption scheme: ")
        data = {"ID": schema_id, "Scheme_Name": schema_name, "key-gen": 'NA', "Symmetric_Key": sym_key, \
                "Public_Key": 'NA', "Private_Key": 'NA'}
        if os.path.exists(myupath + "/config/"):
            with open(myupath + "/config/scheme.json", "w") as write_file:
                json.dump(data, write_file)
        else:
            os.makedirs(myupath + "/config/")
            with open(myupath + "/config/scheme.json", "w") as write_file:
                json.dump(data, write_file)


def view_schema():
    global schema_id
    global schema_name
    global sym_key
    try:
        with open(myupath + "/config/scheme.json", "r") as read_file:
            while True:
                print("WARNING: Sensitive information will be displayed on the screen. Continue? [Y/n]")
                ch = input()
                if ch == 'Y':
                    break
                else:
                    return
            print("Current Schema")
            print("")
            data = json.load(read_file)
            schema_id = data['ID']
            schema_name = data['Scheme_Name']
            sym_key = data['Symmetric_Key']
            print("Schema ID: " + str(schema_id))
            print("Scheme Name: " + schema_name)
            print("Symmetric Key: " + sym_key)
    except FileNotFoundError:
        print("No configuration set")


def dump_schema_file(filename):
    with open(filename, 'w+') as dump_file:
        try:
            with open(myupath + "/config/scheme.json", "r") as read_file:
                data = json.load(read_file)
                dump_file.write(data['Scheme_Name'])
                dump_file.write("\n")
                dump_file.write(data['Symmetric_Key'])
        except:
            print("Encryption schema not set.")

def dump_schema():
    view_schema()

def config_delete():
    global username
    global password
    try:
        with open(myupath + "/config/config.json", "r") as read_file:
            data = json.load(read_file)
            username = data['username']
            password = data['password']
            print("User logged in: " + username)
            check_pass = getpass.getpass("Enter your password to logout: ")
            if check_pass == password:
                os.remove(myupath + "/config/config.json")
                print("Succesfully logged out.")
            else:
                print("Authentication failed.")
                return None
    except FileNotFoundError:
        print("No configuration set")


def config_edit():
    global login_status
    while True:
        usern = input("Username: ")
        passwd = getpass.getpass("Password: ")
        pass_check = getpass.getpass("Confirm password: ")
        if passwd == pass_check:
            break
        else:
            print("Passwords do not match")
    login_status = True
    data = {"username": usern, "password": passwd, "login": login_status}
    if os.path.exists(myupath + "/config/"):
        with open(myupath + "/config/config.json", "w") as write_file:
            json.dump(data, write_file)
    else:
        os.makedirs(myupath + "/config/")
        with open(myupath + "/config/config.json", "w") as write_file:
            json.dump(data, write_file)

    # with open(myupath + "/config/config.json", "w") as write_file:
    #     json.dump(data, write_file)

def status():
    global username
    global password
    global login_status
    global server_url
    global domain
    global observe_path
    count = 0
    try:
        with open(myupath + "/config/config.json", "r") as read_file:
            data = json.load(read_file)
            username = data['username']
            password = data['password']
            login_status = data['login']
            print("The current user is: " + username)
    except FileNotFoundError:
        count = count + 1
        print("No user logged in")
    try:
        with open(myupath + "/config/url.json", "r") as read_file:
            data = json.load(read_file)
            server_url = data['server_url']
            domain = data['domain']
            print("Currently connected to: " + server_url)
    except FileNotFoundError:
        count = count + 1
        print("Server not set-up")
    try:
        with open(myupath + "/config/path.json", 'r') as read_file:
            data = json.load(read_file)
            observe_path = data['observe_path']
            print("Currently observing: " + os.path.abspath(observe_path))
    except:
        count = count + 1
        print("Directory not set-up")
    print("-----------------")
    if count == 0:
        get_status(username, password, observe_path, server_url, domain)
    else:
        print("Configure SPC completely to see status of your files.")

def sync():
    global username
    global password
    global login_status
    global server_url
    global domain
    global observe_path
    read_schema()
    try:
        with open(myupath + "/config/config.json", "r") as read_file:
            data = json.load(read_file)
            username = data['username']
            password = data['password']
            login_status = data['login']
    except FileNotFoundError:
        print("No user logged in")
        return None
    try:
        with open(myupath + "/config/url.json", "r") as read_file:
            data = json.load(read_file)
            server_url = data['server_url']
            domain = data['domain']
    except FileNotFoundError:
        print("Server not set-up")
        return None
    try:
        with open(myupath + "/config/path.json", 'r') as read_file:
            data = json.load(read_file)
            observe_path = data['observe_path']
    except:
        print("Directory not set-up")
        return None
    try:
        auth = coreapi.auth.BasicAuthentication(username=username, password=password, domain=domain)
        client = coreapi.Client(auth=auth)
        document = client.get("http://" + server_url + "/schema/")
    except:
        print("Authentication failed")
        return None

    print("Choose spc sync approach:")
    print("1. Mirror local directory to server")
    print("2. Merge Server and disk contents and perform overwrites on server")
    print("3. Merge Server and disk contents and perform overwrites on client")
    print("")


    while True:
        ch = input("Enter choice[1-3] or s to show status: ")
        if ch in ['1', '2', '3']:
            if ch == '1':
                isactive = requests.post(
                    'http://' + server_url + '/active/?beginsync=' + urllib.parse.quote_plus(username))
                active_stat = isactive.json()['active']
                # print(active_stat)
                if active_stat:
                    print('Sorry, syncing from another machine')
                    return None
                delete()
                upload()
            elif ch == '2':
                isactive = requests.post(
                    'http://' + server_url + '/active/?beginsync=' + urllib.parse.quote_plus(username))
                active_stat = isactive.json()['active']
                # print(active_stat)
                if active_stat:
                    print('Sorry, syncing from another machine')
                    return None
                upload()
                download()
            else:
                isactive = requests.post(
                    'http://' + server_url + '/active/?beginsync=' + urllib.parse.quote_plus(username))
                active_stat = isactive.json()['active']
                # print(active_stat)
                if active_stat:
                    print('Sorry, syncing from another machine')
                    return None
                download()
                upload()
            break
        elif ch == 's':
            status()
        else:
            print("Invalid option")
    requests.post('http://'+server_url + '/active/?endsync=' + urllib.parse.quote_plus(username))


def observe(path):
    path = os.path.abspath(path)
    data = {"observe_path": path}

    if os.path.exists(myupath + "/config/"):
        with open(myupath + "/config/path.json", "w") as write_file:
            json.dump(data, write_file)
    else:
        os.makedirs(myupath + "/config/")
        with open(myupath + "/config/path.json", "w") as write_file:
            json.dump(data, write_file)

    # with open(myupath + "/config/path.json", "w") as write_file:
    #     json.dump(data, write_file)
    #
    print("Now observing  " + path)


def set_url():
    url = input("Enter domain: ")
    port_number = input("Enter port: ")
    sys_url = url + ":" + port_number
    data = {"server_url": sys_url, "domain": url}

    if os.path.exists(myupath + "/config/"):
        with open(myupath + "/config/url.json", "w") as write_file:
            json.dump(data, write_file)
    else:
        os.makedirs(myupath + "/config/")
        with open(myupath + "/config/url.json", "w") as write_file:
            json.dump(data, write_file)

    # with open(myupath + "/config/url.json", "w") as write_file:
    #     json.dump(data, write_file)

    print("Connecting to " + sys_url)


def scheme():
    with open(myupath + "/config/scheme.json", "r") as read_file:
        data = json.load(read_file)


def disconnect():
    server_url = None
    try:
        os.remove(myupath + '/config/url.json')
        print("Disconnected.")
    except:
        print("Disconnected.")

def upload():
    global username
    global password
    global login_status
    global server_url
    global domain
    global observe_path
    read_schema()
    # count = 0
    try:
        with open(myupath + "/config/config.json", "r") as read_file:
            data = json.load(read_file)
            username = data['username']
            password = data['password']
            login_status = data['login']
    except FileNotFoundError:
        print("No user logged in")
        return None
    try:
        with open(myupath + "/config/url.json", "r") as read_file:
            data = json.load(read_file)
            server_url = data['server_url']
            domain = data['domain']
    except FileNotFoundError:
        print("Server not set-up")
        return None
    try:
        with open(myupath + "/config/path.json", 'r') as read_file:
            data = json.load(read_file)
            observe_path = data['observe_path']
    except:
        print("Directory not set-up")
        return None

    sync2(username, password, observe_path, server_url, domain)


def download():
    pbar=ProgressBar()
    # key = password # Temporary
    global username
    global password
    global server_url
    global domain
    global observe_path
    read_schema()
    if schema_id==1:
        from aes import decrypt
    elif schema_id==2:
        from arc4 import decrypt
    elif schema_id==3:
        from blowfish import decrypt
    count = 0
    mismatch = 0
    try:
        with open(myupath + "/config/config.json", "r") as read_file:
            data = json.load(read_file)
            username = data['username']
            password = data['password']
            login_status = data['login']
    except FileNotFoundError:
        print("No user logged in")
        return None
    try:
        with open(myupath + "/config/url.json", "r") as read_file:
            data = json.load(read_file)
            server_url = data['server_url']
            domain = data['domain']
    except FileNotFoundError:
        print("Server not set-up")
        return None
    try:
        with open(myupath + "/config/path.json", 'r') as read_file:
            data = json.load(read_file)
            observe_path = data['observe_path']
    except:
        print("Directory not set-up")
        return None
    try:
        auth = coreapi.auth.BasicAuthentication(username=username, password=password, domain=domain)
        client = coreapi.Client(auth=auth)
        document = client.get("http://" + server_url + "/schema/")
    except:
        print("Authentication failed")
        return None
    userlist = client.action(document, ['users', 'list'])
    user_id = None
    for obj in userlist['results']:
        if obj['username'] == username:
            user_id = obj['id']
            break
    if user_id == None:
        print("User " + username + " has not signed up")
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
    # print(file_list)
    for file_dict in pbar(file_list):
        if (file_dict['owner'] == username):
            file_name = file_dict['file_name']
            file_name = "/" + file_name
            file_name = "/".join(file_name.strip("/").split('/')[1:])
            file_name = observe_path + "/" + file_name
            # print(file_name)
            abspath = Path(file_name)
            # print(abspath)
            if abspath.is_file():
                md5offile = md5sum(abspath)
                if md5offile == file_dict['md5sum']:
                    pass
                else:
                    print(str(abspath) + " is being downloaded")
                    # with open(abspath, 'w', encoding='utf-8') as fOut:
                    #     fOut.write(file_dict['file_data'])
                    #print(file_dict['file_data'])
                    count = count + 1
                    decrypt(str(abspath), literal_eval(file_dict['file_data']), sym_key)
                    local_md = md5sum(str(abspath))
                    server_md = file_dict['md5sum']
                    if local_md != server_md:
                        mismatch = mismatch + 1
            else:
                if os.path.exists(str(abspath)):
                    pass
                else:
                    if file_dict['file_type'] == "DIR":
                        os.makedirs(str(abspath))
                    else:
                        print(str(abspath) + " is being downloaded")
                        # with open(abspath, 'w', encoding='utf-8') as fOut:
                        #     fOut.write(file_dict['file_data'])
                        count = count + 1
                        decrypt(str(abspath), literal_eval(file_dict['file_data']), sym_key)
                        local_md = md5sum(str(abspath))
                        server_md = file_dict['md5sum']
                        if local_md != server_md:
                            mismatch = mismatch + 1
    if count == 0:
        print("Local directory already up-to-date")
    else:
        if mismatch != 0:
            print("Files were not downloaded correctly, please check your connection.")
        else:
            print("Files were downloaded correctly and verified with md5sum")

def delete():
    pbar=ProgressBar()
    print("Preparing server for mirror.")
    # key = password # Temporary
    global username
    global password
    global server_url
    global domain
    global observe_path
    try:
        with open(myupath + "/config/config.json", "r") as read_file:
            data = json.load(read_file)
            username = data['username']
            password = data['password']
            login_status = data['login']
    except FileNotFoundError:
        print("No user logged in")
        return None
    try:
        with open(myupath + "/config/url.json", "r") as read_file:
            data = json.load(read_file)
            server_url = data['server_url']
            domain = data['domain']
    except FileNotFoundError:
        print("Server not set-up")
        return None
    try:
        auth = coreapi.auth.BasicAuthentication(username=username, password=password, domain=domain)
        client = coreapi.Client(auth=auth)
        document = client.get("http://" + server_url + "/schema/")
    except:
        print("Authentication failed.")
        return None
    userlist = client.action(document, ['users', 'list'])
    user_id = None
    for obj in userlist['results']:
        if obj['username'] == username:
            user_id = obj['id']
            break
    if user_id == None:
        print("User " + username + " has not signed up")
        return None
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
    # print(file_list)
    for file_dict in pbar(file_list):
        if (file_dict['owner'] == username):
            file_name = file_dict['file_name']
            client.action(document, ['filedatabase', 'delete'], params={'id': file_dict['id']})
    # print(document)

def login():
    try:
        with open(myupath + "/config/config.json", "r") as read_file:
            data = json.load(read_file)
            username = data['username']
            password = data['password']
            login_status = data['login']
    except FileNotFoundError:
        print("Use config --edit to login")
    try:
        with open(myupath + "/config/url.json", "r") as read_file:
            data = json.load(read_file)
            server_url = data['server_url']
            domain = data['domain']
    except FileNotFoundError:
        print("Use server --set_url to connect.")
    try:
        auth = coreapi.auth.BasicAuthentication(username=username, password=password, domain=domain)
        client = coreapi.Client(auth=auth)
        document = client.get("http://" + server_url + "/schema/")
    except:
        print("Authentication failed.")
        return None
    print(document)
    # client.action(document, ['users', 'list'])

def server_info():
    try:
        with open(myupath + "/config/url.json", "r") as read_file:
            data = json.load(read_file)
            server_url = data['server_url']
            domain = data['domain']
            print("Server IP: " + domain)
            print("Port Number: " +  server_url.replace(domain + ":", ''))
    except FileNotFoundError:
        print("Use server --set_url to connect.")

def signup():
    while (True):
        usern = input("Username: ")
        passwd = getpass.getpass("Password: ")
        pass_check = getpass.getpass("Confirm password: ")
        if passwd == pass_check:
            break
        else:
            print("Passwords do not match")


def list_schemes():
    print("Available encryption schemes")
    print("     1. AES")
    print("     2. ARC4")
    print("     3. Blowfish")

if __name__ == '__main__':
    args = parser.parse_args()
    if args.status:
        status()
    if args.sync:
        sync()
    if args.observe:
        observe(args.observe)
    if args.login:
        login()
    if args.download:
        download()
    if args.upload:
        upload()
    if args.delete:
        delete()
    if args.sub == 'server':
        if args.set_url:
            set_url()
        elif args.disconnect:
            disconnect()
        else:
            server_info()
    if args.sub == 'config':
        if args.edit:
            config_edit()
        if args.delete:
            config_delete()
    if args.sub == 'en-de':
        if args.list:
            list_schemes()
        if args.update:
            if args.file:
                update_scheme_file(args.file)
            else:
                update_schema()
        if args.dump:
            if args.file:
                dump_schema_file(args.file)
            else:
                dump_schema()
        if args.view:
            view_schema()