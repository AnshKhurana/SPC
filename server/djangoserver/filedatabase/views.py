import hashlib
import json
import time
import urllib
from ast import literal_eval

from django import db
from django.contrib.auth.forms import UserCreationForm
import sqlite3
from django.db.models import QuerySet
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse

from djangoserver.settings import STATIC_URL
from filedatabase.models import FileRecord
from filedatabase.permissions import IsOwner
from filedatabase.serializers import FileSerializer, UserSerializer
from rest_framework import generics, viewsets, renderers, status
from django.contrib.auth.models import User
from rest_framework import permissions


class FileViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = FileRecord.objects.all()
    serializer_class = FileSerializer
    permission_classes = (IsOwner,)

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = (AllowAny,)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'filedatabase': reverse('file-list', request=request, format=format)
    })


@api_view(['POST'])
@permission_classes((IsAdminUser,))
def create_user(request):
    serialized = UserSerializer(data=request.data)
    if serialized.is_valid():
        serialized.save()
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = '/'
    template_name = 'signup.html'


def redir_home(request):
    if request.user.is_authenticated:
        return redirect('/home/')
    else :
        return redirect('/login/')


def md5calc(request):
    db = sqlite3.connect('db.sqlite3')
    cur = db.cursor()
    ownerid = request.GET['ownerid']
    filename = request.GET['filename']
    cur.execute("SELECT file_data from filedatabase_filerecord where owner_id=? and file_name=?", [ownerid, filename])
    data = literal_eval(cur.fetchall()[0][0])
    md5 = hashlib.md5(data).hexdigest()
    return HttpResponse(json.dumps({"md5":md5}))


def filedisp(request):
    curruser = request.user
    db = sqlite3.connect('db.sqlite3')
    cur = db.cursor()
    cur.execute("SELECT file_name FROM filedatabase_filerecord order by id limit 1")
    try:
        root = cur.fetchall()[0][0].split('/')[0]
    except:
        raise Http404("No files exist")
    html = ""
    filedata = "b''"
    filetype = ""
    isnotdir = 'false'
    if 'filename' not in request.GET or request.GET['filename'] == root:
        filename = root
    else:
        filename = request.GET['filename']
        html = html + "<a class='btn btn-info btn-lg' href='/files/?filename=" + urllib.parse.quote_plus('/'.join(filename.split('/')[:-1])) + \
                      "'>Back</a><br><br>\n"

    cur.execute("SELECT * FROM filedatabase_filerecord where file_name=? and owner_id=?", [filename, curruser.id])
    obj = cur.fetchall()
    if len(obj) == 0 and filename != root:
        raise Http404('File does not exist')
    if filename == root:
        cur.execute("SELECT file_name,file_type FROM filedatabase_filerecord where owner_id=? and file_name not like '%/%/%'",
                    [curruser.id])
        files = cur.fetchall()
        html = html + "<ul>"
        for f in files:
            if f[1] == 'DIR':
                html = html + "<li><span class='glyphicon glyphicon-folder-open'></span> <a " \
                              "style='word-wrap: break-word' href='/files/?filename=" + urllib.parse.quote_plus(f[0])\
                       + "'>" + f[0].split('/')[-1] + "</a><br>\n"
            else:
                html = html + "<li><span class='glyphicon glyphicon-file'></span> <a style='word-wrap: break-word'" \
                              " href='/files/?filename=" + urllib.parse.quote_plus(
                                f[0]) + "'>" + f[0].split('/')[-1] + "</a><br>\n"
    else:
        file = obj[0]
        if file[4] == "DIR":
            cur.execute("SELECT file_name,file_type FROM filedatabase_filerecord where owner_id=? and file_name "
                        "like ? || '/%' and file_name not like ? || '/%/%'", [curruser.id, filename, filename])
            files = cur.fetchall()
            html = html + "<ul>"
            for f in files:
                if f[1] == 'DIR':
                    html = html + "<li><span class='glyphicon glyphicon-folder-open'></span> <a " \
                                  "style='word-wrap: break-word' href='/files/?filename=" + urllib.parse.quote_plus(
                                    f[0]) + "'>" + \
                           f[0].split('/')[-1] + "</a><br>\n"
                else:
                    html = html + "<li><span class='glyphicon glyphicon-file'></span> <a style='word-wrap: break-word'" \
                                  " href='/files/?filename=" + urllib.parse.quote_plus(
                        f[0]) + "'>" + f[0].split('/')[-1] + "</a><br>\n"
        else:
            filetype = file[4]
            filedata = file[6][2:-1]
            isnotdir = 'true'

    return render(request, 'files.html', {'html': html, 'root': root, 'filetype': filetype, 'filedata':
                  filedata.replace('"', '\\"'), 'isnotdir': isnotdir, 'filename': filename.split('/')[-1]})


def activecheck(request):
    with open('active.json','r') as f:
        active_users = json.load(f)
        # print(active_users)
    arg = True
    if 'beginsync' in request.GET:

        if active_users.get(request.GET['beginsync']) and (active_users[request.GET['beginsync']] + 60 < time.time()):
            db.connections.close_all()
            active_users.__delitem__(request.GET['beginsync'])
        if not active_users.get(request.GET['beginsync']):
            # print('yo')
            active_users.update({request.GET['beginsync']: time.time()})
            arg = False

    if 'endsync' in request.GET:
        try:
            active_users.__delitem__(request.GET['endsync'])
        except KeyError:
            pass

    if 'updatetime' in request.GET:
        if active_users.get(request.GET['updatetime']):
            active_users[request.GET['updatetime']] = time.time()
    # print(active_users)
    with open('active.json','w') as f:
        json.dump(active_users, f)

    return HttpResponse(json.dumps({'active': arg}))
