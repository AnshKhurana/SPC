# SPC Server

SPC server is a Django based server employing Django rest API.

## Setting up and running the server

### Making migrations and migrating changes

First go to the server/djangoserver folder and run the following commands:-

```
	$ python3 manage.py makemigrations
	$ python3 manage.py migrate
```

### For running the server so that the clients can communicate with it

In the server/djangoserver folder run

```
	$ python3 manage.py runserver 0.0.0.0:<port>
```

### IP address and links

For local server the server URL will be 127.0.0.1:8000
This URL will be the URL of the home page of our web-client.