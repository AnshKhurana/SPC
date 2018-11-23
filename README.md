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
(Note that at any point of time you can see your saved settings and your files if any by running the command spc --status from the terminal)

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

    $ spc server --set_url
    Enter domain: <Domain url, for example: 127.0.0.1>
    Enter port:   <Current port, for example 8000>

#### Observing a directory:
    
    $ spc --observe <observe path>


#### 


1. See the version of the software that you are using by running spc --version
2. Signup using the web client setting a username and password for yourself
3. Save your login credentials on your machine for any future use by spc --login and doin as prompted
4. Set the target directory whose files are to be stored on server using spc --observe
5. Set up the url of the server by spc --set_url
6. Choose among any of the 3 encryption schemes available and a strong key for it using spc --update 
7. Sync using any of the 3 options available using spc --sync
8. You may also perform explicit upload, download and delete operations(see man-page for details)
IMPORTANT:-
1. If at any point of time you feel that your security is being compromised you can change the encryption scheme and key in one step without any hassle using spc --update
2. If you need to change the server-url etc you can do so by using spc --edit

# Race Conditions
Please note that you may not be the only one using the services of the server. Working along the lines of first-come and first serve basis if any other user is changing his/her files then you may not be able to do the same concurrently. You are advised to wait for a minute and retry.

# Web-Client
If there is any requirement to view your files remotely from a web-browser then that can also be done easily using our web-client. Just give you spc user credentials, the encryption schema and key and enjoy the rendering of all common file formats saved by you like text, image, pdf, audio and some formats of video.

# Disclaimer
Though you completely free to upload any format of file you can possibly think of but not all may be rendered by the web-client. Though we are working upon this issue and will come up with an update soon!=
