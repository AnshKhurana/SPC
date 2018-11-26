# SPC (Secure Personal Cloud)
Secure Personal Cloud(or SPC as it is called) is a cloud based file storage system like dropbox where the user can choose among three of the encryption schemes provided by the developers, namely:- AES, ARC4, Blowfish.

The cloud is safe and secure to store any confidential information as the server has no knowledge about the encryption schemes and keys. This is a complete Zero-Knowledge based server.

# Installation
From the client folder, use the install.sh script.
```
    $ ./install.sh
```
Note: The sript requires execution permissions and sudo permissions for installation.

If it doesn't work try:
```
    $ chmod +x install.sh
    $ ./install.sh
```

# Usage and Functionalities
The following are the various steps that you need to follow to create a personal space on the server and getting started with storing your sensitive files:-
Note: At any point of time you can see your saved settings and your files if any by running the command spc --status from the terminal)

Note: Before logging in you must sign-up on our web-client

## Linux-Client
 
### General commands

#### SPC Version
```
    $ spc --version
```
#### SPC Help
```
    $ spc --help
```
### Setup

Use the following commands to enter your credentials and configure your cloud.   
    
#### Adding credentials

Changing/adding your credentials 
```
    $ spc config --edit
    Username: <username>
    Password: <password>
    Confirm password: <password>
```
Deleting currently saved credentials
``` 
    $ spc config --delete
```
#### Connecting to the server

View current status:

```
    $ spc server
```

Setting the url:
```
    $ spc server --set_url
    Enter domain: <Domain url, for example: 127.0.0.1>
    Enter port:   <Current port, for example 8000>
```
Disconnecting from the url:
```
    $ spc server --disconnect
```
#### Observing a directory:
```    
    $ spc --observe <observe path>
```
### Setting/updating encryption schemes

#### Print list of available encryption schemes:
```
    $ spc en-de --list
```
#### Update/set an encryption scheme:

1. By entering the details on the terminal
```
    $ spc en-de --update
```
2. By using a schema file
```
    $ spc en-de --update -f <path of the schema file>
```
#### Displaying/saving current encryption scheme:

1. To display the scheme on the terminal
```
    $ spc en-de --dump
```
2. To dump the encryption scheme in the given file
```
    $ spc en-de --dump -f <path of the file>
```
### Syncing files with your SPC:

#### Sync with a given strategy:

To sync with your SPC, enter the following command and choose any of the offered syncing strategies.
```
    $ spc --sync 
    Choose spc sync approach:
    1. Mirror local directory to server
    2. Merge Server and disk contents and perform overwrites on server
    3. Merge Server and disk contents and perform overwrites on client

    Enter choice[1-3] or s to show status: <your choice>
```
#### Advanced usage:

The following commands should be used with caution. 

1. Upload your files to the server (performs overwrites on the server):
```
    $ spc --upload
```
2. Download files from the server (performs overwrites on the client):
```
    $ spc --download
```
3. Delete all files on the server:
```
    $ spc --delete
```
## Race Conditions
Please note that you cannot use more than one client to sync with the server. If one client is already modifying the database, no client of the  same user would be able to connect.

## Web-Client

You can easily sign-up and login on our web-client. The url of the web client is specified by the server. If running locally, enter 127.0.0.1:8000 in your web browser.

If there is any requirement to view your files remotely from a web-browser then that can also be done easily using our web-client. Just give your spc user credentials, the encryption schema and key and enjoy the rendering of all common file formats saved by you like text, image, pdf, audio and some formats of video.

## SPC Server

SPC server is a Django based server employing Django rest API.

### Setting up and running the server

#### Making migrations and migrating changes

First go to the server/djangoserver folder and run the following commands:-

```
    $ python3 manage.py makemigrations
    $ python3 manage.py migrate
```

#### Running the server

In the server/djangoserver folder run

```
    $ python3 manage.py runserver 0.0.0.0:<port>
```

### IP address and links

For local server the server URL will be 127.0.0.1:8000
This URL will be the URL of the home page of our web-client.

<!-- # Disclaimer

Though you completely free to upload any format of file you can possibly think of but not all may be rendered by the web-client. Though we are working upon this issue and will come up with an update soon!=
 -->