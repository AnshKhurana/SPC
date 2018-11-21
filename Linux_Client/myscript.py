import argparse
import coreapi
import getpass
import json
import os
import hashlib
from pathlib import Path
from sync import sync2
from aes import decrypt

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


myupath=os.path.expanduser('~') # work around

parser.add_argument("--status", help="Current status of client", action="store_true")
parser.add_argument("--sync", help="Syncs the user with the client.", action="store_true")
parser.add_argument('--version', action='version', version='%(prog)s 0.7')
parser.add_argument("--observe", help="Observe a directory")
parser.add_argument("--login", help="Check if fields are filled", action="store_true")
parser.add_argument("--download", action="store_true", help="A subprocess to download the files - has to be removed")
parser.add_argument("--upload", action="store_true", help="A subprocess to upload the files - has to be removed")

subparsers = parser.add_subparsers(help='Specify secondary options', dest='sub')

parser_server = subparsers.add_parser("server", help='Server sub-commands')
parser_ende = subparsers.add_parser('en-de', help='en-de sub-commands')
parser_config = subparsers.add_parser('config', help='config sub-commands')


parser_server.add_argument('--set_url', action="store_true", help="Set up url of the server")
parser_server.add_argument('--disconnect', action="store_true", help="Remove server")

parser_ende.add_argument('--list', action="store_true")
parser_ende.add_argument('--update', action="store_true")
parser_ende.add_argument('--dump', action="store_true")
parser_ende.add_argument('--file', '-f')
parser_ende.add_argument('--view', action='store_true')

parser_config.add_argument('--delete', action="store_true")
parser_config.add_argument('--edit', action='store_true')

# subparsers_level2 = parser_ende.add_subparsers(help='sub options for encryption and decryption', dest='ende')
# parser_update = subparsers_level2.add_parser('update', help="update scheme options")
# parser_dump = subparsers_level2.add_parser('dump', help="dump current scheme")
#
# parser_update.add_argument('-f', '--file')
# parser_dump.add_argument('-f', '--file')


def md5sum(filename):
    with open(filename, 'rb') as file_to_check:
        # read contents of the file
        data = file_to_check.read()
        # pipe contents of the file through
        md5_returned = hashlib.md5(data).hexdigest()
        return md5_returned

def update_scheme_file(filename):
    print("Encryption schema has been updated according to " + filename)


def update_schema():
    print("Schema update")
    list_schemes()
    print("")
    IDS = {"RSA" : 4, "AES" : 1, "ACR4" : 2, "Blowfish" : 3}
    while True:
        schema_name = input("Enter a scheme name: ")
        if schema_name in ['RSA', 'AES', 'ACR4', 'Blowfish']:
            break
        else:
            print("Schema name is not valid, enter the scheme name from the above list(case sensitive)")
    schema_id = IDS[schema_name]
    sym_key = input("Enter the key for your encryption scheme: ")
    data = {"ID": schema_id, "Scheme_Name": schema_name, "key-gen": 'NA', "Symmetric_Key": 'NA', \
            "Public_Key": 'NA', "Private_Key": 'NA'}
    if os.path.exists(myupath + "/config/"):
        with open(myupath + "/config/scheme.json", "w") as write_file:
            json.dump(data, write_file)
    else:
        os.makedirs(myupath + "/config/")

def view_schema():
    print("Current Schema")
    try:
        with open(myupath + "/config/scheme.json", "r") as read_file:
            while True:
                print("WARNING: Sensitive information will be displayed on screen. Continue? [Y/n]")
                ch = input()
                if ch == 'Y':
                    break
                else:
                    return
            data = json.load(read_file)
            schema_id = data['ID']
            schema_name = data['Scheme_Name']
            sym_key = data['Symmetric Key']
            print("Schema ID:" + schema_id)
            print("Scheme Name:" + schema_name)
            print("")
    except FileNotFoundError:
        print("No configuration set")

def config_delete():
    try:
        with open(myupath+"/config/config.json", "r") as read_file:
            data = json.load(read_file)
            username = data['username']
            password = data['password']
            print("User logged in: " + username)
            check_pass = getpass.getpass("Enter your password to logout: ")
            if check_pass == password:
                os.remove(myupath+"/config/config.json")
                print("Succesfully logged out.")
            else:
                print("Authentication failed.")
    except FileNotFoundError:
        print("No configuration set")

def config_edit():
    while(True):
        usern = input("Username: ")
        passwd = getpass.getpass("Password: ")
        pass_check = getpass.getpass("Confirm password: ")
        if passwd == pass_check:
            break
        else:
            print("Passwords do not match")
    login_status = True
    data = {"username" : usern, "password" : passwd, "login" : login_status}
    with open(myupath+"/config/config.json", "w") as write_file:
        json.dump(data, write_file)

def status():
    try:
        with open(myupath+"/config/config.json", "r") as read_file:
            data = json.load(read_file)
            username = data['username']
            password = data['password']
            login_status = data['login']
            print("The current user is: " + username)
    except FileNotFoundError:
        print("No user logged in")
    try:
        with open(myupath+"/config/url.json", "r") as read_file:
            data = json.load(read_file)
            server_url = data['server_url']
            domain = data['domain']
            print("Currently connected to: " + server_url)
    except FileNotFoundError:
        print("Server not set-up")
    try:
        with open(myupath+"/config/path.json", 'r') as read_file:
            data = json.load(read_file)
            observe_path = data['observe_path']
            print("Currently observing: " + os.path.abspath(observe_path))
    except:
        print("Directory not set-up")


def sync():
    if (login and server_url):
        auth = coreapi.auth.BasicAuthentication(username=username, password=password, domain=domain)
        client = coreapi.Client(auth=auth)
        document = client.get("http://" + server_url + "/schema/")
        print(document.url)
        print(type(document))
    else:
        print("You need to login first")
    print("To be implemented")


def observe(path):
    data = {"observe_path": path}
    with open(myupath+"/config/path.json", "w") as write_file:
        json.dump(data, write_file)
    print("Now observing  " + path)


def set_url():
    url = input("Enter domain: ")
    port_number = input("Enter port: ")
    sys_url = url + ":" + port_number
    data = {"server_url": sys_url, "domain" : url}
    with open(myupath+"/config/url.json", "w") as write_file:
        json.dump(data, write_file)
    print("Connecting to " + sys_url)

def scheme():
    with open(myupath+"/config/scheme.json", "r") as read_file:
        data = json.load(read_file)

def disconnect():
    server_url = None
    os.remove(myupath+'/config/url.json')
    print("Disconnected")

def upload():
    try:
        with open(myupath+"/config/config.json", "r") as read_file:
            data = json.load(read_file)
            username = data['username']
            password = data['password']
            login_status = data['login']
    except FileNotFoundError:
        print("No user logged in")
    try:
        with open(myupath+"/config/url.json", "r") as read_file:
            data = json.load(read_file)
            server_url = data['server_url']
            domain = data['domain']
    except FileNotFoundError:
        print("Server not set-up")
    try:
        with open(myupath+"/config/path.json", 'r') as read_file:
            data = json.load(read_file)
            observe_path = data['observe_path']
    except:
        print("Directory not set-up")
    sync2(username, password, observe_path, server_url, domain)


def download():
   # key = password # Temporary
    try:
        with open(myupath+"/config/config.json", "r") as read_file:
            data = json.load(read_file)
            username = data['username']
            password = data['password']
            login_status = data['login']
    except FileNotFoundError:
        print("No user logged in")
    try:
        with open(myupath+"/config/url.json", "r") as read_file:
            data = json.load(read_file)
            server_url = data['server_url']
            domain = data['domain']
    except FileNotFoundError:
        print("Server not set-up")
    try:
        with open(myupath+"/config/path.json", 'r') as read_file:
            data = json.load(read_file)
            observe_path = data['observe_path']
    except:
        print("Directory not set-up")
    auth = coreapi.auth.BasicAuthentication(username=username, password=password, domain=domain)
    client = coreapi.Client(auth=auth)
    document = client.get("http://" + server_url + "/schema/")
    userlist = client.action(document, ['users', 'list'])
    user_id = None
    for obj in userlist['results']:
        if obj['username'] == username:
            user_id = obj['id']
            break
    if  user_id == None:
        print("User " + username + " has not signed up")
    file_list = client.action(document, ['filedatabase', 'list'])
    file_list = file_list['results']
    #print(file_list)
    for file_dict in file_list:
        if (file_dict['owner'] == username):
            file_name = file_dict['file_name']
            file_name = os.path.abspath(file_name)
            abspath = Path(file_name)
            if abspath.is_file():
                md5offile = md5sum(abspath)
                if md5offile == file_dict['md5sum']:
                    pass
                else:
                    print(str(abspath) + " is being downloaded")
                    with open(abspath, 'w', encoding='utf-8') as fOut:
                        fOut.write(file_dict['file_data'])
                    #decrypt(str(abspath), password)
            else:
                if os.path.exists(str(abspath)):
                    pass
                else:
                    if file_dict['file_type'] == "DIR":
                        os.makedirs(str(abspath))
                    else:
                        print(str(abspath) + " is being downloaded")
                        with open(abspath, 'w', encoding='utf-8') as fOut:
                            fOut.write(file_dict['file_data'])
                       # decrypt(str(abspath), password)
def login():
    try:
        with open(myupath+"/config/config.json", "r") as read_file:
            data = json.load(read_file)
            username = data['username']
            password = data['password']
            login_status = data['login']
    except FileNotFoundError:
        print("Use config --edit to login")
    try:
        with open(myupath+"/config/url.json", "r") as read_file:
            data = json.load(read_file)
            server_url = data['server_url']
            domain = data['domain']
    except FileNotFoundError:
        print("Use server --set_url <url> to connect.")
    auth = coreapi.auth.BasicAuthentication(username=username, password=password, domain=domain)
    client = coreapi.Client(auth=auth)
    document = client.get("http://" + server_url + "/schema/")
    print(document)
    client.action(document, ['users', 'list'])

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
    print("     2. ACR4")
    print("     3. Blowfish")
    print("     4. RSA")


def dump_schema_file(filename):
    print("Current schema dumped to " + filename)


def dump_schema():
    print("To be implemented")


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
    if args.sub =='server':
        if args.set_url:
            set_url()
        if args.disconnect:
            disconnect()
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

    # if args.sub == 'en-de':
    #     if args.ende == 'update':
    #         if args.file:
    #             update_scheme_file(args.file)
    #         else:
    #             update_schema()
    #     if args.ende == 'dump':
    #         if args.file:
    #             dump_schema_file(args.file)
    #         else:
    #             dump_schema()
    #     if args.list:
    #         list_schemes()
    #
    #
