# SPC(Secure Personal Cloud)
Secure Personal Cloud(or SPC as it is called) is a cloud based file storage system like dropbox where the user can choose among three of the encryption schemes provided by the developers, namely:- AES, ARC4, Blowfish.

The cloud is safe and secure to store any confidential information as the server has no knowledge about the encryption schemes and keys. This is a complete Zero-Knowledge based server.

# Installation
From the SPC folder, use the install.sh script.

    $ ./install.sh

Note: The sript requires execution permissions and sudo permissions for installation.

If it doesn't work try:

    $ chmod +x install.sh
    $ ./install.sh


# Usage and Functionalities
The following are the various steps that you need to follow to create a personal space on the server and getting started with storing your sensitive files:-
Note: At any point of time you can see your saved settings and your files if any by running the command spc --status from the terminal)

Note: Before logging in you must sign-up on our web-client

## Linux-Client
 
### General commands

#### SPC Version

    $ spc --version
#### SPC Help

    $ spc --help

### Setup

Use the following commands to enter your credentials and configure your cloud.   
    
#### Adding credentials

Changing/adding your credentials 

    $ spc config --edit
    Username: <username>
    Password: <password>
    Confirm password: <password>

Deleting currently saved credentials
    
    $ spc config --delete

#### Connecting to the server

Setting the url:

    $ spc server --set_url
    Enter domain: <Domain url, for example: 127.0.0.1>
    Enter port:   <Current port, for example 8000>

Disconnecting from the url:
    $ spc server --disconnect

#### Observing a directory:
    
    $ spc --observe <observe path>

### Setting/updating encryption schemes

#### Print list of available encryption schemes:

    $ spc en-de --list

#### Update/set an encryption scheme:

    1. By entering the details on the terminal

        $ spc en-de --update

    2. By using a schema file

        $ spc en-de --update -f <path of the schema file>

#### Displaying/saving current encryption scheme:

    1. To display the scheme on the terminal

        $ spc en-de --dump

    2. To dump the encryption scheme in the given file

        $ spc en-de --dump -f <path of the file>
### Syncing files with your SPC:

To sync with your SPC, enter the following command and choose any of the offered syncing strategies.

    $ spc --sync 


## Race Conditions
Please note that you cannot use more than one client to sync with the server. Working along the lines of first-come and first serve basis if any other machine(client) of yours is changing the files then you may not be able to do the same concurrently.

6. Choose among any of the 3 encryption schemes available and a strong key for it using spc --update 
7. Sync using any of the 3 options available using spc --sync
8. You may also perform explicit upload, download and delete operations(see man-page for details)
 to wait for a minute and retry.

# Web-Client
If there is any requirement to view your files remotely from a web-browser then that can also be done easily using our web-client. Just give you spc user credentials, the encryption schema and key and enjoy the rendering of all common file formats saved by you like text, image, pdf, audio and some formats of video.

# Disclaimer
Though you completely free to upload any format of file you can possibly think of but not all may be rendered by the web-client. Though we are working upon this issue and will come up with an update soon!=
